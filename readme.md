# AI Deployer
- [AI Deployer](#ai-deployer)
- [English documentation / Documentación en Ingles](#english-documentation--documentación-en-ingles)
  - [Introduction](#introduction)
  - [Searching for a Pipeline](#searching-for-a-pipeline)
  - [Searching for a Model](#searching-for-a-model)
  - [Getting Started](#getting-started)
    - [Launching Container: `docker run -p 80:80 -e PIPELANE=<pipeline_name> ai-deployer`](#launching-container-docker-run--p-8080--e-pipelanepipeline_name-ai-deployer)
- [Spanish documentation / Documentación en Español](#spanish-documentation--documentación-en-español)
  - [Introducción](#introducción)
  - [Buscando un modelo](#buscando-un-modelo)
  - [Eligiendo una pipeline](#eligiendo-una-pipeline)
  - [Como empezar](#como-empezar)
    - [Montar contenedor: `docker run -p 80:80 -e PIPELANE=<nombre_de_la_pipeline> ai-deployer`](#montar-contenedor-docker-run--p-8080--e-pipelanenombre_de_la_pipeline-ai-deployer)
# English documentation / Documentación en Ingles

## Introduction
ai-deployer is a tool designed to democratize access to artificial intelligence, enabling users without technical knowledge and novice programmers to deploy Python APIs integrating artificial intelligence models available on Hugging Face with just one command. This project facilitates the experimentation and rapid deployment of AI solutions for specific tasks, opening a range of possibilities in various areas such as text analysis, content generation, image recognition, among others.

To deploy the project, you will need to specify a Hugging Face pipeline; for more complex requirements, you can specify the model too.

## Searching for a Pipeline
Pipelines are predefined interfaces that simplify interaction with the models. Here is a list of the main ones.

WARNING: If no model is specified, but a pipeline is, the system will choose the default model for that pipeline.

- "sentiment-analysis": For sentiment analysis.
- "text-generation": For text generation.
- "feature-extraction": For feature extraction.
- "fill-mask": To complete masked parts of text.
- "ner" (Named Entity Recognition): For recognizing named entities.
- "question-answering": To answer questions given a context.
- "summarization": To summarize long texts.
- "translation_xx_to_yy": For translation between languages, where xx and yy are ISO language codes.
- "zero-shot-classification": For text classification without the need for specific training labels.
- "conversational": To build conversations.

You can find a complete and updated list of available pipelines in the Hugging Face Transformers documentation.

## Searching for a Model
To find a model on Hugging Face that fits your needs, visit the Hugging Face website and use the search bar to find models by name, task type, or language. Review the model's documentation and usage examples to ensure it meets your expectations.


## Getting Started
- Clone repository: `git clone https://github.com/M3str3/Easy-open-model-deployer.git`
- Build image: `docker build -t ai-deployer`.

### Launching Container: `docker run -p 80:80 -e PIPELANE=<pipeline_name> ai-deployer`
  - Replace <pipeline_name> with the name of the pipeline you wish to use, for example, fill-mask.

----

# Spanish documentation / Documentación en Español

## Introducción
`ai-deployer` es una herramienta diseñada para democratizar el acceso a la inteligencia artificial, permitiendo a usuarios sin conocimientos técnicos y a programadores novatos desplegar APIs de Python que integran modelos de inteligencia artificial disponibles en Hugging Face con un solo comando. Este proyecto facilita la experimentación y el despliegue rápido de soluciones de IA para tareas específicas, abriendo un abanico de posibilidades en diversas áreas como análisis de texto, generación de contenido, reconocimiento de imágenes, entre otros.

Para desplegar el proyecto necesitaras especificar una pipelane, para cuestiones mas complejas puedes especificar el modelo.

## Buscando un modelo
Para buscar un modelo en Hugging Face que se ajuste a tus necesidades, visita el sitio web de [Hugging Face](https://huggingface.co/models) y utiliza la barra de búsqueda para encontrar modelos por nombre, tipo de tarea, o lenguaje. Revisa la documentación del modelo y los ejemplos de uso para asegurarte de que cumple con tus expectativas.

## Eligiendo una pipeline
Las pipelines son interfaces predefinidas que simplifican la interacción con los modelos. Aqui te dejo un listado de las principales.

ADVERTENCIA: si no se especifica modelo, pero si pipelane, el sistema elegira el modelo predeterminado para esa pipelane.

- "sentiment-analysis": Para análisis de sentimiento.
- "text-generation": Para generación de texto.
- "feature-extraction": Para extracción de características.
- "fill-mask": Para completar partes enmascaradas de texto.
- "ner" (Named Entity Recognition): Para reconocimiento de entidades nombradas.
- "question-answering": Para responder preguntas dadas un contexto.
- "summarization": Para resumir textos largos.
- "translation_xx_to_yy": Para traducción entre idiomas, donde xx y yy son códigos de idioma ISO.
- "conversational": Para construir conversaciones.


Puedes encontrar una lista completa y actualizada de las pipelines disponibles en la documentación de Hugging Face Transformers.

## Como empezar
- Copiar repositorio: `git clone https://github.com/M3str3/Easy-open-model-deployer.git`
- Construir imagen: `docker build -t ai-deployer .`

### Montar contenedor: `docker run -p 80:80 -e PIPELANE=<nombre_de_la_pipeline> ai-deployer`
  - Ejemplo: `docker run -p 80:80 -e PIPELANE=sentiment-analysis ai-deployer`
  - Reemplaza <nombre_de_la_pipeline> con el nombre de la pipeline que deseas utilizar, por ejemplo, fill-mask.
  

