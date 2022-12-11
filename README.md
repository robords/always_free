# Always Free

What can a Python hobbiest build without spending a dime?

## Stable Diffusion
1. Make sure you install PyTorch first
2. Set up your account on Hugging Face https://huggingface.co/welcome
3. Accept the license aggreement to run it locally: https://huggingface.co/runwayml/stable-diffusion-v1-5
4. Clone it locally: https://github.com/huggingface/diffusers/tree/main#running-the-model-locally
5. Cross fingers
6. Chunk it, since you probably don't have the GPU or CPU:
```python
import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-5",
    revision="fp16", 
    torch_dtype=torch.float16)

# Try: disable the following line if you run on CPU
# On mac "mps" (otherwise, "cuda", if there is a Nvidia GPU)
pipe = pipe.to("mps")

prompt = "a photo of an astronaut riding a horse on mars"
pipe.enable_attention_slicing()
image = pipe(prompt).images[0] # This took about 4 minutes on Macbook Air
image.save("./static/astronaut_rides_horse.png")
```


OR try running it not locally:
```python
import os
import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", 
    torch_dtype=torch.float16, 
    revision="fp16",
    use_auth_token=os.environ['HUGGING_FACE_TOKEN']) 
    # This took about 2 minutes on Macbook Air
    # it downloads the pretrained model into memory, ~2 GB
    # Don't forget to run `export HUGGING_FACE_TOKEN="<token>"`

# On mac "mps" (otherwise, "cuda", if there is a Nvidia GPU)
pipe = pipe.to("mps")

prompt = "a photo of a bluebird riding a horse on mars"
image = pipe(prompt).images[0] # This took 3.5 minutes on Macbook Air
image.save("./static/bluebird_rides_horse.png")
```

If you run into memory issues, try lowering the resolution, i.e. add "-W 256 -H 256"