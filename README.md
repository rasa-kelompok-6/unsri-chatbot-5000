# rasa-chatbot

Unsri chatbot 5000

Feature:
<ol>
    <li>Menanyakan tentang ketentuan-ketentuan sebagai mahasiswa Universitas Sriwijaya</li>
    <li>Custom actions untuk menambahkan nama</li>
    <li>Custom actions untuk menanyakan waktu sekarang</li>
    <li>Database sqlite untuk memasukkan nama, nim, semester, dan ipk</li>
</ol>

# Steps before usage

## Install anaconda

[Windows](https://www.anaconda.com/products/individual#windows)

[Any other OS](https://docs.anaconda.com/anaconda/install/)

# Run
Open anaconda prompt

Go to target directory with anaconda prompt. Example `cd Desktop\rasa-chatbot`

Check available environments with `conda info --envs`, or create one with `conda create --name 'env-name' python=='version'`. Example `conda create --name RasaInstall python==3.8`

Activate with `conda activate 'env-name'`, example `conda activate RasaInstall`

## If you create a new environment
run `conda install ujson`, `conda install tensorflow`, `pip install --upgrade pip=20.2 --user`, and `pip install rasa`.

### If you want to have rasa x
instead of `pip install rasa`

run 

`pip install rasa==2.8.2`, 

`pip install rasa-sdk==2.8.1`, 

`pip install rasa-x==0.39.3 --extra-index-url https://pypi.rasa.com/simple`, 

`pip3 install SQLAlchemy==1.3.22`,

`pip install --upgrade pyparsing==2.4.7`,

and `pip install sanic-jwt==1.6.0` (Newer version of rasa x seems to always crash, so just install past versions)

If you want a new project, then initialize with `rasa init`

## Once rasa is installed
In one terminal, run `rasa run actions`

And then open another terminal and do the following:

`rasa run -m models --enable-api --cors "*" --endpoints endpoints.yml` to run on browser. Then open index.html on browser

`rasa shell --endpoints endpoints.yml` to run on shell

`rasa train` if you want to train model with new data

`rasa x --endpoints endpoints.yml` to run rasa x, built in browser GUI by rasa