import numpy as np
from quiver_engine import server
from torchvision import  models
from quiver_engine.model_utils import register_hook

import threading

if __name__ == "__main__":
    
    model = models.vgg19(pretrained=False)
    hook_list = register_hook(model)

    thread = threading.Thread(target=server.launch, args=(model, hook_list, "./data/Cat",False, [200,200], ))
    thread.daemon = True
    thread.start()

    while True:
        a = input("input:")

        if a == '0':
            break
        elif a == '1':
            print("resnet")
            model = models.resnet18(pretrained=False)
            hook_list = register_hook(model) 
            server.update_model(model, hook_list, "./data/Dog", [200,200])
        elif a == '2':
            print("vgg19")
            model = models.vgg19(pretrained=False)
            hook_list = register_hook(model) 
            server.update_model(model, hook_list, "./data/Cat", [200,200])
    