# Place for test data

## USGS Gazetteer Data

Gazetteer data can be downloaded from https://geonames.usgs.gov/domestic/download_data.htm
See under 'States, Territories, Associated Areas of the United States' You can select an individual state, 
a National File with all the features in one zip file, or an All States file with 
individual state files in one zip file. The data is a pipe-delimited file in UTF-8 encoded 
text format. Additional detail on the file format can accessed by clicking the File Format link.


## NGA Gazetteer Data

Gazetteer data can be downloaded from http://earth-info.nga.mil/gns/html/namefiles.htm

The data are in tab-delimited files in UTF-8 encoded text format. The fields containing names information (SHORT_FORM, GENERIC, FULL_NAME_RO, FULL_NAME_RG, and NOTE) are encoded using UTF-8.

Additional detail on the field names and descriptions can be found here:
http://earth-info.nga.mil/gns/html/gis_countryfiles.html

## Google POI Example

from Google Maps Javascript API v3:
https://developers.google.com/maps/documentation/javascript/places#place_details

**Place Details Results**

A successful getDetails() call returns a PlaceResult object with the following properties:

- address_components: The collection of address components for this Place's location. See the Geocoding service's Address Component Types section for more details.
- formatted_address: The Place's full address.
- formatted_phone_number: The Place's phone number, formatted according to the number's regional convention.
- geometry: The Place's geometry-related information. This includes:
  - location provides the latitude and longitude of the Place.
  - viewport defines the preferred viewport on the map when viewing this Place.
- html_attributions: Attribution text to be displayed for this Place result.
- icon: URL to an image resource that can be used to represent this Place's type.
- id: contains a unique identifier denoting this place. This identifier may not be used to retrieve information about this place, but can be used to consolidate data about this Place, and to verify the identity of a Place across separate searches. As ids can occasionally change, it's recommended that the stored id for a Place be compared with the id returned in later Details requests for the same Place, and updated if necessary.
- international_phone_number contains the Place's phone number in international format. International format includes the country code, and is prefixed with the plus (+) sign. For example, the international_phone_number for Google's Sydney, Australia office is +61 2 9374 4000.
- name: The Place's name.
- utc_offset contains the number of minutes this Place’s current timezone is offset from UTC. For example, for Places in Sydney, Australia during daylight saving time this would be 660 (+11 hours from UTC), and for Places in California outside of daylight saving time this would be -480 (-8 hours from UTC).
- opening_hours contains the following information:
  - open_now is a boolean value indicating if the Place is open at the current time.
  - periods[] is an array of opening periods covering seven days, starting from Sunday, in chronological order. Each period contains:
    - open contains a pair of day and time objects describing when the Place opens:
      - day a number from 0–6, corresponding to the days of the week, starting on Sunday. For example, 2 means Tuesday.
      - time may contain a time of day in 24-hour hhmm format (values are in the range 0000–2359). The time will be reported in the Place’s timezone.
    - close may contain a pair of day and time objects describing when the Place closes. Note: If a Place is always open, the close section will be missing from the response. Applications can rely on always-open being represented as an open period containing day with value 0 and time with value 0000, and no close.
- photos[]: an array of PlacePhoto objects. A PlacePhoto can be used to obtain a photo with the getUrl() method, or you can inspect the object for the following values:
  - height: the maximum height of the image, in pixels.
  - width: the maximum width of the image, in pixels.
  - html_attributions: Attribution text to be displayed with this Place photo.
- rating: The Place's rating, from 0.0 to 5.0, based on user reviews.
- reference contains a token that can be used to query the Details service in future. This token may differ from the reference used in the request to the Details service. It is recommended that stored references for Places be regularly updated. Although this token uniquely identifies the Place, the converse is not true: a Place may have many valid reference tokens.
- reviews an array of up to five reviews. Each review consists of several components:
  - aspects[] contains an array of PlaceAspectRating objects, each of which provides a rating of a single attribute of the establishment. The first object in the array is considered the primary aspect. Each PlaceAspectRating is defined as:
    - type the name of the aspect that is being rated. The following types are supported: appeal, atmosphere, decor, facilities, food, overall, quality and service.
    - rating the user's rating for this particular aspect, from 0 to 3.
  - author_name the name of the user who submitted the review. Anonymous reviews are attributed to "A Google user". If a language parameter was set, then the phrase "A Google user" will return a localized string.
  - author_url the URL to the users Google+ profile, if available.
  - language an IETF language code indicating the language used in the user's review. This field contains the main language tag only, and not the secondary tag indicating country or region. For example, all the English reviews are tagged as 'en', and not 'en-AU' or 'en-UK' and so on.
  - rating the user's overall rating for this Place. This is a whole number, ranging from 1 to 5.
  - text the user's review. When reviewing a location with Google Places, text reviews are considered optional; therefore, this field may by empty.
- types: An array of types for this Place (e.g., ["political", "locality"] or ["restaurant", "establishment"]).
- url: URL of the associated Google Place Page.
- vicinity: A simplified address for the Place, including the street name, street number, and locality, but not the province/state, postal code, or country. For example, Google's Sydney, Australia office has a vicinity value of 5/48 Pirrama Road, Pyrmont. The vicinity property is only returned for a Nearby Search.
- website lists the authoritative website for this Place, such as a business' homepage.



## OSUK POI Example

A POI sample can be downloaded at the bottom of this page: http://www.ordnancesurvey.co.uk/business-and-government/licensing/sample-data/discover-data.html

"Unique_Reference_Number"|"Name"|"PointX_Classification_Code"|"Feature_Easting"|"Feature_Northing"|"Positional_Accuracy_Code"|"UPRN"|"Topographic_TOID"|"Topographic_TOID_Version"|"ITN_Easting"|"ITN_Northing"|"ITN_TOID"|"ITN_TOID_Version"|"Distance"|"Address_Detail"|"Street_Name"|"Locality"|"Geographic_County"|"Postcode"|"Verified_Address"|"Administrative_Boundary"|"Telephone_Number"|"URL"|"Brand"|"Qualifier_Type"|"Qualifier_Data"|"Provenance"|"Date_of_Supply"|"POSTCODE_2"|"UPP"|"PC_AREA"|"POSTCODE_2_2"|"UPP_2"|"PC_AREA_2"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2RE"|"00004000000001601524"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2NS"|"00004000000000484208"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 5AF"|"00004000000000484523"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2AF"|"00004000000000484068"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2LQ"|"00004000000000484188"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2ND"|"00004000000000484197"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2NY"|"00004000000000484213"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2BL"|"00004000000000484090"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2AA"|"00004000000000484064"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 5AD"|"00004000000000484522"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2HS"|"00004000000000484153"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2LJ"|"00004000000000484184"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2LR"|"00004000000000484189"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2AE"|"00004000000000484067"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2JE"|"00004000000000484162"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2AB"|"00004000000000484065"|"EX"
14358187|"Exwick Barton"|"03190259"|290357.5|94979.6|"1"|""|"1000000347785322"|5|"290497.6"|"94970.9"|"4000000025450925"|"1"|"140.3"|""|""|""|"Devon"|"EX4"|"N"|"Exeter District"|""|""|""|""|""|"Ordnance Survey"|"01-MAR-2012"|"EX4 2AF"|"00004000000000484068"|"EX"|"EX4 2LW"|"00004000000000484193"|"EX"


where POSITIONAL_ACCURACY_LOOKUP =
https://github.com/opengeospatial/poi/blob/master/testdata/osuk/positional_accuracy_lookup.bsv

where POI_CLASSIFICATIONS = 
https://github.com/opengeospatial/poi/blob/master/testdata/osuk/poi_classifications.bsv

where POI_CLASS_TO_SIC_LOOKUP = 
https://github.com/opengeospatial/poi/blob/master/testdata/osuk/poi_class_to_sic_lookup.bsv

where POI_GROUPS =
https://github.com/opengeospatial/poi/blob/master/testdata/osuk/poi_groups.bsv

where POI_CATEGORIES = 
https://github.com/opengeospatial/poi/blob/master/testdata/osuk/poi_categories.bsv

where KEYWORDS =
https://github.com/opengeospatial/poi/blob/master/testdata/osuk/keywords.bsv

where ADMINISTRATIVE_BOUNDARY_LOOKUP = 
https://github.com/opengeospatial/poi/blob/master/testdata/osuk/administrative_boundary_lookup.bsv