#### QuiverPytorch: interactive CNN visualization tool for pytorch

##### Install：



##### Usage:

```python
import numpy as np
from quiver_engine import server
from quiver_engine.model_utils import register_hook
from torchvision import  models

if __name__ == "__main__":
    model = models.resnet18() # define model

    hook_list = register_hook(model) # register hook function for conv. layers
    
    server.launch(model, hook_list, input_folder="./data/Cat") # start 
```

open web browser and input url: http://localhost:5000/ 

![](./doc/vis.png)

##### Todo：

- [ ] parameterize image size for visualization
- [ ] show network output 

##### Reference：

- https://github.com/keplr-io/quiver
- https://github.com/szagoruyko/pytorchviz/tree/master/

