from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from MongoClient import writetodb


# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = '54957b9bac3940ccbc6f0846d0f61061'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = '5gcxbtbki5o4'
APP_ID = 'FoodTest'
# Change these to whatever model and image URL you want to use
MODEL_ID = 'food-item-recognition'
MODEL_VERSION_ID = '1d5fd481e0cf4826aa72ec3ff049e044'
IMAGE_URL = 'https://www.iheartnaptime.net/wp-content/uploads/2023/01/how-to-make-granola.jpg'

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

post_model_outputs_response = stub.PostModelOutputs(
    service_pb2.PostModelOutputsRequest(
        user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
        model_id=MODEL_ID,
        version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        url=IMAGE_URL
                    )
                )
            )
        ]
    ),
    metadata=metadata
)
if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
    # print(post_model_outputs_response.status)
    raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

# Since we have one input, one output will exist here
output = post_model_outputs_response.outputs[0]

##Predicted concepts

for concept in output.data.concepts:
    value = concept.value
    # print("%s %.2f" % (concept.name, concept.value))


# Uncomment this line to print the full Response JSON
    for json in output.data.concepts:
        if json.value > .90:
            resultFound = {"id": json.id, "name": json.name}
            # print("Result")
            # print(json)
            writetodb(resultFound)

# print(output)