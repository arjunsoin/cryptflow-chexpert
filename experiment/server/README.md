# Server instructions

### EzPC Setup:
```
cd ~/
git clone https://github.com/mpc-msri/EzPC.git
cd EzPC
./setup_env_and_build.sh quick
```

### Compile the model:
```
source ~/EzPC/mpc_venv/bin/activate
```
Compiling the model (will take ~20 mins):
```
python ~/EzPC/Athos/CompileONNXGraph.py --config config.json --role server
```
This generates:
- `model_SCI_HE.out`: The binary with the MPC protocol.
- `model_input_weights_fixedpt_scale_15.inp`: Model weights to be fed as input to the binary.
- `client.zip`: This contains:
   - `config.json`: The compilation config file.
   - `optimised_model.onnx`: The model with the weights stripped off.

We will send this `client.zip` to the client. Since the model is pruned, it doesn't reveal any propreitary weights to the client and only the model structure i.e. the computation. The client will then compile this model using CrypTFlow and generate the MPC binary.

### Experiment setup:
2. Copy experiment.tar to /data1/ and then:
	```
    cd /data1/
	tar -xf experiment.tar
	```
3. Copy `model_SCI_HE.out` and `model_input_weights_fixedpt_scale_15.inp` to `/data1/experiment/`
4. Update `EZPC_PATH` in `preprocess_images.sh` and `run_2pc.sh` if you didn't clone EzPC in ~/ directory.

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
   Here role=1 for server and =2 for client. eg: ```bash run_2pc.sh 1 192.168.1.1 32000```
