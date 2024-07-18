namespace py example

service ExampleService {
  string ping(1: map<string, string> headers),
  string sayHello(1: map<string, string> headers, 2: string name)
}
