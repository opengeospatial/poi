import sqlite3
import json
import os

def extract_ea_model(qea_file_path, output_json_path):
    """
    Extract model information from an Enterprise Architect .qea file
    and convert it to JSON format that can be used to create a JSON schema.
    
    Args:
        qea_file_path: Path to the .qea file
        output_json_path: Path where the output JSON will be saved
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(qea_file_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Extract classes (tables in most models)
    cursor.execute("""
        SELECT o.Object_ID, o.Name, o.Note, o.Stereotype
        FROM t_object o
        WHERE o.Object_Type = 'Class'
    """)
    classes = [dict(row) for row in cursor.fetchall()]
    
    # For each class, get its attributes (properties in JSON Schema)
    model_data = {}
    for cls in classes:
        class_id = cls['Object_ID']
        cursor.execute("""
            SELECT a.ID, a.Name, a.Type, a.Notes, a.Length, a.Precision, 
                   a.Scale, a.LowerBound, a.UpperBound, a.Default
            FROM t_attribute a
            WHERE a.Object_ID = ?
        """, (class_id,))
        attributes = [dict(row) for row in cursor.fetchall()]
        
        # Get relationships
        cursor.execute("""
            SELECT c.Connector_ID, c.Start_Object_ID, c.End_Object_ID, 
                   c.Connector_Type, c.Name, c.Notes
            FROM t_connector c
            WHERE c.Start_Object_ID = ? OR c.End_Object_ID = ?
        """, (class_id, class_id))
        relationships = [dict(row) for row in cursor.fetchall()]
        
        # Store all related data
        model_data[cls['Name']] = {
            'id': cls['Object_ID'],
            'name': cls['Name'],
            'description': cls['Note'],
            'stereotype': cls['Stereotype'],
            'attributes': attributes,
            'relationships': relationships
        }
    
    # Close the connection
    conn.close()
    
    # Write the extracted model data to a JSON file
    with open(output_json_path, 'w') as f:
        json.dump(model_data, f, indent=2)
    
    return model_data

def convert_to_json_schema(model_data, output_schema_path):
    """
    Convert the extracted EA model data to a JSON Schema.
    
    Args:
        model_data: Dictionary containing the EA model data
        output_schema_path: Path where the JSON Schema will be saved
    """
    # Create a basic schema structure
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Generated from EA model",
        "description": "JSON Schema generated from Enterprise Architect model",
        "definitions": {},
        "type": "object",
        "properties": {}
    }
    
    # Add each class as a definition and property
    for class_name, class_data in model_data.items():
        # Create a schema definition for this class
        class_schema = {
            "type": "object",
            "title": class_name,
            "description": class_data.get('description', ''),
            "properties": {},
            "required": []
        }
        
        # Add attributes as properties
        for attr in class_data.get('attributes', []):
            property_name = attr['Name']
            property_schema = {
                "description": attr.get('Notes', '')
            }
            
            # Map EA types to JSON Schema types
            ea_type = attr.get('Type', '').lower()
            if 'int' in ea_type or 'number' in ea_type:
                if 'decimal' in ea_type or 'float' in ea_type or 'double' in ea_type:
                    property_schema["type"] = "number"
                else:
                    property_schema["type"] = "integer"
            elif 'bool' in ea_type:
                property_schema["type"] = "boolean"
            elif 'date' in ea_type or 'time' in ea_type:
                property_schema["type"] = "string"
                property_schema["format"] = "date-time"
            else:
                property_schema["type"] = "string"
            
            # Handle min/max length for strings
            if property_schema["type"] == "string" and attr.get('Length'):
                try:
                    max_length = int(attr['Length'])
                    if max_length > 0:
                        property_schema["maxLength"] = max_length
                except (ValueError, TypeError):
                    pass
            
            # Add default value if specified
            if attr.get('Default'):
                property_schema["default"] = attr['Default']
            
            # Check if property is required
            lower_bound = attr.get('LowerBound', '0')
            if lower_bound and lower_bound != '0':
                class_schema["required"].append(property_name)
            
            # Add the property to the class schema
            class_schema["properties"][property_name] = property_schema
        
        # Add the class schema to definitions
        schema["definitions"][class_name] = class_schema
        
        # Add a reference to this class in the root properties
        schema["properties"][class_name] = {"$ref": f"#/definitions/{class_name}"}
    
    # Write the JSON Schema to a file
    with open(output_schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    return schema

# Example usage:
if __name__ == "__main__":
    qea_file = "path/to/your/model.qea"
    intermediate_json = "ea_model_data.json"
    json_schema_output = "generated_schema.json"
    
    # Extract the EA model data
    model_data = extract_ea_model(qea_file, intermediate_json)
    
    # Convert the extracted data to a JSON Schema
    convert_to_json_schema(model_data, json_schema_output)
    
    print(f"JSON Schema successfully generated at {json_schema_output}")