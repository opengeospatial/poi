import xml.etree.ElementTree as ET
import json
import argparse
import os
import re
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("xmi2json")

def safe_get_text(element, xpath, default="", namespaces=None):
    """Safely get text from an XML element using XPath."""
    try:
        result = element.findtext(xpath, default, namespaces)
        return result if result is not None else default
    except Exception as e:
        logger.debug(f"Error getting text with XPath {xpath}: {e}")
        return default

def safe_find_all(element, xpath, namespaces=None):
    """Safely find all elements matching XPath."""
    try:
        result = element.findall(xpath, namespaces)
        return result if result is not None else []
    except Exception as e:
        logger.debug(f"Error finding elements with XPath {xpath}: {e}")
        return []

def detect_xmi_version(root):
    """Detect XMI version from the root element."""
    # Try to determine XMI version
    xmi_version = root.get('{http://schema.omg.org/spec/XMI/2.1}version') or \
                 root.get('xmi:version') or \
                 "2.1"  # Default to 2.1 if not found
                 
    logger.info(f"Detected XMI version: {xmi_version}")
    return xmi_version

def get_namespaces(root):
    """Extract namespaces from the root element."""
    namespaces = {}
    
    # Extract namespaces from the root element attributes
    for key, value in root.attrib.items():
        if key.startswith("xmlns:"):
            prefix = key.split(":")[-1]
            namespaces[prefix] = value
    
    # Add common namespaces if not already present
    common_namespaces = {
        'xmi': 'http://schema.omg.org/spec/XMI/2.1',
        'uml': 'http://schema.omg.org/spec/UML/2.1',
        'UML': 'org.omg.xmi.namespace.UML'  # For older EA exports
    }
    
    for prefix, uri in common_namespaces.items():
        if prefix not in namespaces:
            namespaces[prefix] = uri
    
    logger.info(f"Using namespaces: {namespaces}")
    return namespaces

def find_classes(root, namespaces):
    """Find all classes in the XMI document using multiple search patterns."""
    classes = []
    
    # Try multiple search patterns based on different EA export versions
    search_patterns = [
        './/packagedElement[@xmi:type="uml:Class"]',
        './/UML:Class',
        './/{http://schema.omg.org/spec/UML/2.1}Class',
        './/Class',
        './/ownedElement[@xmi:type="uml:Class"]'
    ]
    
    for pattern in search_patterns:
        try:
            found_classes = safe_find_all(root, pattern, namespaces)
            if found_classes:
                logger.info(f"Found {len(found_classes)} classes using pattern: {pattern}")
                classes.extend(found_classes)
        except Exception as e:
            logger.debug(f"Error searching with pattern {pattern}: {e}")
    
    # If still no classes found, try a more generic approach for EA-specific formats
    if not classes:
        logger.info("No classes found with standard patterns, trying EA-specific search")
        try:
            # Look for elements that might represent classes
            all_elements = root.findall(".//*")
            for element in all_elements:
                element_type = element.get("xmi:type") or element.tag.split("}")[-1]
                if element_type in ["Class", "uml:Class"]:
                    classes.append(element)
            
            if classes:
                logger.info(f"Found {len(classes)} classes using generic search")
        except Exception as e:
            logger.debug(f"Error in generic search: {e}")
    
    return classes

def get_class_attributes(cls, namespaces):
    """Find all attributes for a class using multiple search patterns."""
    attributes = []
    
    # Try multiple search patterns based on different EA export versions
    search_patterns = [
        './ownedAttribute',
        './/Attribute',
        './/attributes/Attribute',
        './/ownedMember[@xmi:type="uml:Property"]',
        './/attribute'
    ]
    
    for pattern in search_patterns:
        try:
            found_attrs = safe_find_all(cls, pattern, namespaces)
            if found_attrs:
                logger.debug(f"Found {len(found_attrs)} attributes using pattern: {pattern}")
                attributes.extend(found_attrs)
                break  # Use the first successful pattern
        except Exception as e:
            logger.debug(f"Error searching attributes with pattern {pattern}: {e}")
    
    return attributes

def get_attribute_type(attr, namespaces):
    """Determine the attribute type from various possible formats."""
    type_name = ""
    
    # Try to get type from different possible locations
    try:
        # Direct type attribute
        type_name = attr.get('type') or ""
        
        if not type_name:
            # Type element reference
            type_element = attr.find('./type', namespaces) or \
                          attr.find('.//type', namespaces) or \
                          attr.find('.//properties', namespaces)
            
            if type_element is not None:
                type_name = type_element.get('xmi:idref', '') or \
                           type_element.get('href', '') or \
                           type_element.get('name', '') or \
                           type_element.get('type', '')
        
        # EA sometimes stores type in a 'properties' tag with a 'type' attribute
        if not type_name:
            properties = attr.find('.//properties')
            if properties is not None:
                type_name = properties.get('type', '')
        
    except Exception as e:
        logger.debug(f"Error determining type: {e}")
    
    # Extract just the type name if it's a reference
    if ':' in type_name:
        type_name = type_name.split(':')[-1]
    
    return type_name.lower()

def map_ea_type_to_json_schema(ea_type):
    """Map Enterprise Architect data types to JSON Schema types."""
    # Strip any array indicators and handle them separately
    is_array = False
    if '[]' in ea_type:
        is_array = True
        ea_type = ea_type.replace('[]', '')
    
    # Integer types
    if any(int_type in ea_type for int_type in ['int', 'long', 'short', 'byte']):
        json_type = "integer"
    # Number types
    elif any(float_type in ea_type for float_type in ['float', 'double', 'decimal', 'real', 'number']):
        json_type = "number"
    # Boolean types
    elif any(bool_type in ea_type for bool_type in ['bool', 'boolean']):
        json_type = "boolean"
    # Date/Time types
    elif any(date_type in ea_type for date_type in ['date', 'time', 'timestamp']):
        json_type = "string"
        format = "date-time"
        return {"type": json_type, "format": format}
    # Default to string
    else:
        json_type = "string"
    
    # Handle arrays
    if is_array:
        return {
            "type": "array",
            "items": {"type": json_type}
        }
    
    return {"type": json_type}

def convert_xmi_to_json_schema(xmi_file_path, output_schema_path):
    """
    Convert an XMI file exported from Enterprise Architect to JSON Schema
    
    Args:
        xmi_file_path: Path to the XMI file
        output_schema_path: Path where the JSON Schema will be saved
    """
    try:
        # Parse the XMI file
        logger.info(f"Parsing XMI file: {xmi_file_path}")
        tree = ET.parse(xmi_file_path)
        root = tree.getroot()
        
        # Detect XMI version and namespaces
        xmi_version = detect_xmi_version(root)
        namespaces = get_namespaces(root)
        
        # Create basic JSON Schema structure
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Generated from EA model",
            "description": "JSON Schema generated from Enterprise Architect XMI export",
            "definitions": {},
            "type": "object",
            "properties": {}
        }
        
        # Find all UML classes
        classes = find_classes(root, namespaces)
        logger.info(f"Found a total of {len(classes)} classes")
        
        if not classes:
            logger.warning("No classes found in the XMI file!")
            
        for cls in classes:
            class_name = cls.get('name')
            if not class_name:
                logger.debug("Skipping class with no name")
                continue
                
            logger.info(f"Processing class: {class_name}")
            
            # Create a definition for this class
            class_schema = {
                "type": "object",
                "title": class_name,
                "description": "",
                "properties": {},
                "required": []
            }
            
            # Get class documentation if available
            description = safe_get_text(cls, './ownedComment/body', '', namespaces) or \
                         safe_get_text(cls, './/documentation', '', namespaces) or \
                         cls.get('documentation', '')
            if description:
                class_schema["description"] = description
            
            # Process attributes
            attributes = get_class_attributes(cls, namespaces)
            logger.info(f"Found {len(attributes)} attributes for class {class_name}")
                     
            for attr in attributes:
                attr_name = attr.get('name')
                if not attr_name:
                    logger.debug("Skipping attribute with no name")
                    continue
                    
                logger.debug(f"Processing attribute: {attr_name}")
                
                # Create property schema
                property_schema = {
                    "description": safe_get_text(attr, './ownedComment/body', '', namespaces) or \
                                  safe_get_text(attr, './/documentation', '', namespaces) or \
                                  attr.get('documentation', '') or ''
                }
                
                # Determine property type
                type_name = get_attribute_type(attr, namespaces)
                logger.debug(f"Attribute {attr_name} has type: {type_name}")
                
                # Map to JSON Schema type
                type_schema = map_ea_type_to_json_schema(type_name)
                property_schema.update(type_schema)
                
                # Check for multiplicity to determine if property is required
                multiplicity = attr.get('multiplicity') or ''
                lower_value = attr.get('lowerBound') or \
                             safe_get_text(attr, './lowerValue/@value', '0', namespaces) or \
                             safe_get_text(attr, './/lower', '0', namespaces) or \
                             '0'
                             
                if lower_value and lower_value != '0':
                    class_schema["required"].append(attr_name)
                
                # Add additional constraints if available
                if property_schema.get("type") == "string":
                    # Look for string length constraints
                    length = attr.get('length', '')
                    if length and length.isdigit():
                        property_schema["maxLength"] = int(length)
                
                # Add the property to the class schema
                class_schema["properties"][attr_name] = property_schema
            
            # Clean up empty required list
            if not class_schema["required"]:
                del class_schema["required"]
            
            # Add the class schema to definitions
            schema["definitions"][class_name] = class_schema
            
            # Add a reference to this class in the root properties
            schema["properties"][class_name] = {"$ref": f"#/definitions/{class_name}"}
        
        # Write the JSON Schema to a file
        with open(output_schema_path, 'w') as f:
            json.dump(schema, f, indent=2)
        
        logger.info(f"JSON Schema successfully generated at {output_schema_path}")
        return schema
    except ET.ParseError as e:
        logger.error(f"Error parsing XMI file: {e}")
        raise
    except Exception as e:
        logger.error(f"Error converting XMI to JSON Schema: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert EA XMI export to JSON Schema')
    parser.add_argument('xmi_file', help='Path to the XMI file exported from Enterprise Architect')
    parser.add_argument('--output', '-o', default='schema.json', help='Output JSON Schema file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        convert_xmi_to_json_schema(args.xmi_file, args.output)
        print(f"JSON Schema successfully generated at {args.output}")
    except Exception as e:
        print(f"Failed to convert XMI to JSON Schema: {e}")
        sys.exit(1)