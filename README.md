# Always Free

* What can I build without spending any money?
* How can we automate it so updates are pushed automatically from my repository?


|                          | **Python Anywhere** | **Oracle VM**                                                                                                                                                                     | 
|--------------------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Memory (GB)              | 3               | 1                                                                                                                                                                                | 
| CPU                      | 100 Seconds     | 1 OCPU                                                                                                                                                                           | 
| Network bandwidth (Gbps) | "Low"           | 0.48                                                                                                                                                                             | 
| Disk Space (GB)          | 0.512           | [50](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm#:~:text=Free%20compute%20instances-,Block%20Volume,-All%20tenancies%20receive) | 

## Python Anywhere
**What's Free?**
There is a free tier, with very limited resources

**How do I automatically update from Github?**
[Github Webhooks](https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664) allows me to push every time there is a change made to Python Anywhere

**Steps:**
1. Install Git
2. Clone your repo to Python Anywhere (this adds your "update_server" path)
3. Create the webhook

## Oracle Cloud

**What's Free?**
There's an ["always free"](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) tier which includes a micro VM for compute.

**How do I automatically update from Github?**
[Github Webhooks again](https://clement.notin.org/blog/2021/04/13/auto-deploy-python-flask-web-app-on-github-push/)

**Steps:**
Roughly following [this tutorial](https://docs.oracle.com/en-us/iaas/developer-tutorials/tutorials/flask-on-ubuntu/01oci-ubuntu-flask-summary.htm#).
1. Create the free-tier VM (Oracle Console)
2. Add ingress rule to VM subnet (Oracle Console)
3. Install Git, `sudo yum install git`
4. Create SSH key for github [walkthrough](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
5. Add SSH key to github [walkthrough](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
6. Clone repo
7. Create and Start venv (`cd ~/always_free && make setup`)
8. Make it easy to start the venv - add an alias to ~/.bashrc or ~/.zshrc: `alias af="cd ~/always_free && source ~/.venv/always_free/bin/activate"`
8. Install requirements.txt: in the venv, `make install`
9. Update the firewall `sudo iptables -I INPUT -m state --state NEW -p tcp --dport 5000 -j ACCEPT`
9. Run it
### Setup nginx on Oracle VM 
To put flask behind nginx, make sure to install python3-devel first: `sudo yum install python3-devel`     

Follow the [tutorial here](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7).
1. `sudo yum install epel-release`
2. `sudo yum install nginx` 
3. Start it: `sudo systemctl start nginx`
4. Get it's status: `sudo systemctl status nginx`
5. Open the firewall: 
```linux
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
```
6. Add ports 80 and 443 to the Security List under virtual cloud networks
7. Verify you see the defaul nginx page at the server public IP 


## Google Cloud
**What's Free?**
There's a free tier, specifically I'm interested in [App Engine](https://cloud.google.com/free/docs/free-cloud-features#app-engine)

How do I keep from exceeding the limit?
WIP


## Features
### Stable Diffusion
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