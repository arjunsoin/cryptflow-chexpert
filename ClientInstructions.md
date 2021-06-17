# Client instructions

### EzPC (language for secure machine learning) Setup:
```
cd ~/
git clone https://github.com/mpc-msri/EzPC.git
cd EzPC
./setup_env_and_build.sh quick
```

### Experiment setup:
1. Set up virtual environment to conduct the experiment:
   ```
   source ~/EzPC/mpc_venv/bin/activate
   ```
2. Copy experiment.tar to /data1/ and then:
	```
    cd /data1/
	tar -xf experiment.tar
	```
3. Put all your input images in /data1/experiment/images directory. Name them such that you are able to compare outputs with ground truth once the experiment has finished running. The exact naming convention you use will be followed by CrypTFlow to create subsequent intermediary inputs (numpy input files, txt files to record memory and computation statistics)

4. Compile the pruned model (model WITHOUT weights) (expected time ~20 mins). The config.json file contains relevant input configurations for the model.
   ```
   unzip client.zip
   python ~/EzPC/Athos/CompileONNXGraph.py --config config.json --role client
   ```
5. Update EZPC_PATH in ```preprocess_images.sh``` and ```run_2pc.sh``` if you have not cloned EzPC in ~/ directory.

6. Preprocess images:
	```
   bash preprocess_images.sh
   ```
   This converts images into fixedpoint input and stores it in scaled_inputs directory.

### Run experiment:
1. Create a persistent tmux session: 
   ```
   tmux new -s chexpert_experiment
   ```
2. 
   ```
   source ~/EzPC/mpc_venv/bin/activate
   ```
3.
   ```
   bash run_2pc.sh ROLE SERVER_IP SERVER_PORT
   ```
   Here role=1 for server and =2 for client. eg: ```bash run_2pc.sh 2 192.168.1.1 32000```
