
# scripts for ClaiFai

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
import requests
import matplotlib.pyplot as plt
from PIL import Image

def Clarifai_Food_Model(stub, metadata, file_bytes, model=None):
    food_model = '9504135848be0dd2c39bdab0002f78e9'
    food_item = 'bd367be194cf45149e75f01d59f77ba7'
    if not model:
        model = food_item
        
    post_model_outputs_response = stub.PostModelOutputs(
    service_pb2.PostModelOutputsRequest(
        model_id=model,
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here.
    
    output = post_model_outputs_response.outputs[0]

    
    rlt = []
    
    for concept in output.data.concepts:
        rlt.append({'name': concept.name, 'value': concept.value})
        
    return(rlt)
        
def Food_Image_Analysis(file_path, stub, metadata):
    
    image = Image.open(file_path)
    plt.imshow(image)
    plt.show()
    
    with open(file_path, "rb") as f:
        img_file = f.read()
        
    output = Clarifai_Food_Model(stub, metadata,img_file)
    
    return(output)

def food_dish_detetion(headers, img):
    # Single Dishes Detection
    url = 'https://api.logmeal.es/v2/recognition/dish'
    resp = requests.post(url,files={'image': open(img, 'rb')}, headers=headers)

    out = resp.json()['recognition_results'][0]

    return out
