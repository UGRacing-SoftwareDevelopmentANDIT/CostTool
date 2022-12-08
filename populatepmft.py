import os
import string
import random
import csv


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'costing-web-app.settings')

import django

django.setup()
from django.core.files import File
from django.db.models import Q
from tool.models import *
from datetime import datetime
from pytz import utc
from django.contrib.auth.models import User


def populate():
    
    pmft_Catagory,material_subtype,indivMaterial = importMaterials("materials.csv")
    
    for i in range(len(pmft_Catagory)):
        pmft_catagory = pmft_Catagory[i]["pmft_catagory"]
        pmft_type = pmft_Catagory[i]["pmft_type"]
        material_subtype_name = material_subtype[i]["material_subtype_name"]
        material_name = indivMaterial[i]["individual_material_name"]
        material_cost = indivMaterial[i]["material_cost"]
        material_cost_comment = indivMaterial[i]["material_cost_comment"]
        material_comment = indivMaterial[i]["material_comment"]
        imeche_name = indivMaterial[i]["imeche_name"]
        
        addMaterial(pmft_catagory,pmft_type,material_subtype_name,material_name,material_cost,material_cost_comment,material_comment,imeche_name)

        
        
        
        

def importMaterials(filename):
    pmftCatagory = []
    materialSubtype = []
    indivMaterial = []
    
    with open(filename, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                catagory = {}
                catagory["pmft_catagory"] = row[2]
                catagory["pmft_type"] = row[0]
                pmftCatagory.append(catagory)
                
                subtype = {}
                subtype["material_subtype_name"] = row[3]
                materialSubtype.append(subtype)
                
                material = {}
                material["individual_material_name"] = row[4]
                material["material_cost"] = row[5]
                material["material_cost_comment"]= row[6]
                material["material_comment"] = row[7]
                material["imeche_name"] = row[1]
                indivMaterial.append(material)
                
    return pmftCatagory,materialSubtype,indivMaterial

def addMaterial(pmft_catagory,pmft_type,material_subtype_name,material_name,material_cost,material_cost_comment,material_comment,imeche_name):
    catagoryObject ,t= PmftCategory.objects.get_or_create(pmftCatagory=pmft_catagory,pmftType=pmft_type)
    catagoryObject.pmftCatagory = pmft_catagory
    catagoryObject.pmftType = pmft_type
    catagoryObject.save()
    
    subtypeObject,t = MaterialSubtype.objects.get_or_create(materialSubtypeName=material_subtype_name)
    subtypeObject.materialSubtypeName = material_subtype_name
    subtypeObject.materialCategoryID = catagoryObject
    subtypeObject.save()
    
    materialObject,t = IndividualMaterial.objects.get_or_create(individualMaterialName=material_name,materialCost=material_cost,materialCostComment=material_cost_comment,imecheName=imeche_name,materialComment=material_comment)
    materialObject.individualMaterialName=material_name
    materialObject.materialCost = material_cost
    materialObject.materialCostComment=material_cost_comment
    materialObject.imecheName = imeche_name
    materialObject.materialComment = material_comment
    materialObject.individualMaterialSubtypeID = subtypeObject
    materialObject.save()
                
if __name__ == '__main__':
    print('Starting population script...')
    populate()
    print('Completed population script, exiting...')

            