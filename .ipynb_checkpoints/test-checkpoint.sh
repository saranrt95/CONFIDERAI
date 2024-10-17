#!/bin/bash

for dataset in $(echo 'p2p' 'ssh' 'smoking' 'cardio' 'platooning' 'rul' 'eeg' 'mqttset' 'telescope' 'fire'); do #'ssh'
	for typetest in $(echo 'true');do
		(python3 ConformalLLM.py $dataset $typetest 1)
	done
done
