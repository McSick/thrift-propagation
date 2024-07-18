# Thrift Example with Context Propagation

This project demonstrates how to set up two services that communicate using Apache Thrift in Python, including passing headers (such as a trace ID) for context propagation.

## Prerequisites

- Python 3.x
- Apache Thrift 0.20.0
- pip (Python package installer)

## Installation

### Step 1: Install Apache Thrift

Download and extract Thrift

### Step 2: Install Python Dependencies

Create a virtual environment and install the required Python packages:

```sh
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### Step 3: Generate Thrift Code

Generate the Python code from the Thrift file:

```sh
thrift --gen py example.thrift
```

## Project Structure

```
thrift-propagation/
├── example.thrift
├── gen-py/
│   └── example/
│       ├── ExampleService.py
│       └── ttypes.py
├── server.py
└── client.py
├── requirements.txt
└── README.md
```

## Running the Example

### Step 1: Run the Server

In one terminal, run the server:

```sh
export HONEYCOMB_API_KEY=your-api-key
python server.py
```

### Step 2: Run the Client

In another terminal, run the client:

```sh
export HONEYCOMB_API_KEY=your-api-key
python client.py
```

The client will send requests to the server with headers
## Thrift Interface Definition

Here is the `example.thrift` file used in this project:

```thrift
namespace py example

service ExampleService {
  string ping(1: map<string, string> headers),
  string sayHello(1: map<string, string> headers, 2: string name)
}
```

## Requirements

The `requirements.txt` file contains the following:

```
thrift==0.20.0
opentelemetry-api==1.25.0
opentelemetry-sdk==1.25.0
opentelemetry-exporter-otlp==1.25.0
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
