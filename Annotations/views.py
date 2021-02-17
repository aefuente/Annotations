from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
import json
from PIL import Image
def index(request):
    return render(request, 'index.html')


def write_header(image,path,f):
    width, height = Image.open(path).size
    
    print("<annotation>",file=f)
    print("    <folder>VOC2007</folder>",file=f)
    print("    <filename>{}</filename>".format(image), file=f)
    print("    <path>/Users/andre/AI_Research/Scale/JPEGImages/{}</path>".format(image),file=f)
    print("    <source>",file=f)
    print("        <database>Unknown</database>",file=f)
    print("    </source>",file=f)
    print("    <size>",file=f)
    print("        <width>{}</width>".format(width),file=f)
    print("        <height>{}</height>".format(height),file=f)
    print("        <depth>3</depth>",file=f)
    print("    </size>",file=f)
    print("    <segmented>0</segmented>",file=f)

def write_object(obj, f):
    print("    <object>",file=f)
    print("        <name>{}</name>".format(obj['name']),file=f)
    print("        <pose>Unspecified</pose>",file=f)
    print("        <truncated>0</truncated>",file=f)
    print("        <difficult>0</difficult>",file=f)
    print("        <bndbox>",file=f)
    print("            <xmin>{}</xmin>".format(obj['x1']),file=f)
    print("            <ymin>{}</ymin>".format(obj['y1']),file=f)
    print("            <xmax>{}</xmax>".format(obj['x2']),file=f)
    print("            <ymax>{}</ymax>".format(obj['y2']),file=f)
    print("        </bndbox>",file=f)
    print("    </object>",file=f)

def write_end(f):
    print("</annotation>",file=f)






def makexml(request):
    xml_path="/home/aefuente/Annotations/Annotations/static/xml/"
    img_path="/home/aefuente/Annotations/Annotations/static/images/"
    

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        image = data['image']
        with open(os.path.join(xml_path,image[:image.find('.')]+'.xml'), 'w') as f:

            write_header(image,os.path.join(img_path,image),f)
            objects= data['objects']
            
            for item in objects:
                name = item[0]
                obj = {'name': name, 'x1' : item[1]['startX'], 'x2' : item[1]['startX']+ item[1]['w'], 'y1' : item[1]['startY'], 'y2' : item[1]['startY'] + item[1]['h']}
                write_object(obj,f)
            write_end(f)

    return HttpResponse(status=201)

def images(request):
    
    img_path="/home/aefuente/Annotations/Annotations/static/images/"
    xml_path="/home/aefuente/Annotations/Annotations/static/xml/"
    
    xml_list = os.listdir(xml_path)
    xml_list = [x[:-4] for x in xml_list]

    img_list = os.listdir(img_path)
    img_list = [x[:-4] for x in img_list]
    
    img_list = list(set(img_list)-set(xml_list))
    img_list = [x +'.jpg' for x in img_list]
    img_list.sort()

    return  render(request, 'images.html', {'images': img_list})
