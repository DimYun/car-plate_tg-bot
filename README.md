## Car plates project. Additional example how to use API service in Telegram bot

This is the project for car plate OCR recognition, which include:
1. [Neural network segmentation model for car plate area with number selection (part 1/3)](https://github.com/DimYun/car-plate-segm_model)
2. [Neural network OCR model for plate character recognition (part 2/3)](https://github.com/DimYun/car-plate-ocr_model)
3. [API service for these two models (part 3/3)](https://github.com/DimYun/car-plate_service)
4. Additional example how to use API service in Telegram bot

A decentralized parking app that automatically pays for parking using geolocation and plate recognition was created 
using an API service. The app was developed during the TON x ETH Belgrade hackathon. For more information, 
check out [the project's presentation](presentation.pdf).

Used technologies:

* Aiogram (for telegram bot)
* Asyncio
* Requests, for communication with API
* CI/CD (test, deploy, destroy)
* Linters (flake8 + wemake, pylint)

**Disclaimers**:

* the project was originally crated and maintained in GitLab local instance, some repo functionality may be unavailable
* the project was created by my team "LogicYield" for TON х ETH Belgrade Hackathon
* according to time limitation main code include in `main.py` file


### Setup of environment

First, create and activate `venv`:
    ```bash
    python3 -m venv venv
    . venv/bin/activate
    ```

Next, install dependencies:
    ```bash
    make install
    ```


### Commands

#### Preparation
* `make install` - install python dependencies

#### Run telegram bot
* `make run_app` - run servie. You can define argument `APP_PORT`

#### Static analyse
* `make lint` - run linters
