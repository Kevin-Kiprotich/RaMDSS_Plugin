import requests
import json
import math
from . import log
from .functions import addVectorLayer, show_error_message

def fetchData(dlg):
    outputPath = dlg.outputLineEdit.text()
    email=dlg.emailLineEdit.text()
    form = dlg.formComboBox.currentText()
    geometry = dlg.geometryComboBox.currentText()
    url = f"http://107.191.43.246:8090/stats_module/mobile_data_fetch/"
    params = {"email": email}
    headers = {
        "accept": "application/json"
    }
    response = requests.post(url=url,headers=headers, params=params, timeout=300)
    if response.status_code==200:
        geojson_object={
            "type":"FeatureCollection",
            "features":[

            ]
        }
        length= len(response.json())
        count = 0
        for entry in response.json():
            count += 1
            if entry['geometry_type'] != geometry or entry['form_title']!=form:
                continue
            properties={
                'id':entry['id'],
                'form_title':entry['form_title'],
                'form_status':entry['form_status'],
                'email':entry['email'],
                "image":entry['image_file'][0] if len(entry['image_file']) != 0 else "",
                "video":entry['video_file'][0] if len(entry['video_file']) != 0 else "",
                'audio':entry['audio_file'][0] if len(entry['audio_file']) != 0 else "",
                'date_time':entry['date_time'] if entry['date_time'] is not None else ""
            }
            geom = {
                "type":geometry.capitalize(),
                "coordinates":[[]] if geometry == "polygon" else []
            }

            for question in entry["questions"]:
                # print(question)
                if question['type'] == 'media':
                    continue
                if question['type'] == "geometry":
                    if len(question['answer']) == 0 or question['answer'] is None:
                        continue
                    if geometry=="polygon":
                        for point in question['answer']:
                            geom['coordinates'][0].append([point[1], point[0]])
                        if geom['coordinates'][0][0] != geom['coordinates'][0][-1]:
                            geom['coordinates'][0].append(geom['coordinates'][0][0])     
                    elif geometry == "point":
                        geom['coordinates']=[question['answer'][1],question['answer'][0]]
                    else:
                        show_error_message("Invalid geometry. Geometry is either point or polygon")
                        
                    continue
                properties[question['question']]=question['answer'] if question['answer'] != "Other" else question['otherAnswer']

            feature = {
                "type":"Feature",
                "properties":properties,
                "geometry": geom
            }
            geojson_object['features'].append(feature)
            
            percentage = math.floor((count/length)*100)
            log(F"Length: {length}")
            log(f"Position: {count}")
            dlg.progressBar.setValue(percentage)
        with open(outputPath, "w") as file:
            json.dump(geojson_object, file, indent=4)
        addVectorLayer(outputPath)
        dlg.progressBar.setValue(100)
    else:
        print(response)
        show_error_message(f"Could not fetch data. Error code:{response.status_code}")