# anvisa-data-dumper
A library for extracting ANVISA data from their website.\
_Uma biblioteca para extração de dados a partir do site da ANVISA._

This repository is still under development and is not stable.

## Features
:heavy_check_mark: Download drugs data\
:x: Download drug details data\
:x: Download drugs leaflets\
:x: Export data as JSON, xlsx and CSV\
:x: Filter data before downloading\
:x: Documentation

## Usage
Clone the repository
```
git clone https://github.com/rafaelmartinsrm/anvisa-data-dumper.git
```

Install the dependencies
```
pip install -r requirements.txt
```

Use it
```
from anvisa_data_dumper.drugs import Drugs
Drugs().dump(threads=4)
```

Each page from ANVISA's API will be downloaded to /cache/drugs/_pagenumber_.json
