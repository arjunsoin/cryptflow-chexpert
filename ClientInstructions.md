# Client instructions

### EzPC Setup:
```
cd ~/
git clone https://github.com/mpc-msri/EzPC.git
cd EzPC
./setup_env_and_build.sh quick
```

### Experiment setup:
1. 
   ```
   source ~/EzPC/mpc_venv
   ```
2. Copy experiment.tar to /data1/ and then:
	```
    cd /data1/
	tar -xf experiment.tar
	```
3. Put all your input images in /data1/experiment/images directory
4. Compile pruned model (model without weights) (will take ~20 mins)
   ```
   unzip client.zip
   python ~/EzPC/Athos/CompileONNXGraph.py --config config.json --role client
   ```
5. Update EZPC_PATH in ```preprocess_images.sh``` and ```run_2pc.sh``` if you didn't clone EzPC in ~/ directory.
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
   source ~/EzPC/mpc_venv
   ```
3.
   ```
   bash run_2pc.sh ROLE SERVER_IP SERVER_PORT
   ```
   Here role=1 for server and =2 for client. eg: ```bash run_2pc.sh 2 192.168.1.1 32000```
