# Samsara Thesis

The following repo contains the code to reproduce my Master Thesis from Samsara Project. 

## Repo Structure

* samsara: Contains notebooks associated to every stage of the Model Training. The code is modularized following this structure:
  * data_utils: Contains utility functions to import and preprocess data. 
  * data_prep: Contains code to format data appropriately to input the model. This process includes Data Split and Training Sequences Creation. 
  * deepant: Contains the code to DeepAnt Pytorch Lightning Implementation. 
    * data: Contains the Dataset and LightningDataModule.
    * model: Contains the DeepAnt Architecture and the LightningModule. 
    * inference: Contains the post-processing to make the model detect anomalies as required. 
    * settings: Contains Trainer instance and Hyperparameter to be used. 
  * evaluation: Contains utility functions to analyze results and generate the ground truth to evaluate the performance of the model. 
  
  * EDA: Contiene un Dashboard interactivo con todo una exploración de datos inicial para entender cómo venía la data inicialmente y cuál es el efecto de los preprocesamientos.
  * test: Some tests to check the Training Sequences Creation Process. 

## Commands

- To visualize the Dashboard use: 

```bash
make dashboard
```
- To execute Tests use: 

```bash
make tests
```
