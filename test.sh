#!/bin/bash

for dataset in $(echo 'p2p' 'ssh' 'smoking' 'cardio' 'platooning' 'rul' 'eeg' 'mqttset' 'telescope' 'fire'); do 
	for typetest in $(echo 'true' 'false');do
		(python3 CONFIDERAI_main.py $dataset $typetest 1)
	done
done
