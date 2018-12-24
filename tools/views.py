# Create your views here.

from django.http import StreamingHttpResponse, HttpResponse


def stream_response_generator(ip):
    from shelljob import proc
    g = proc.Group()
    p = g.run(["bash", "-c", "nmap %s -sV -vvvv"%ip])

    while g.is_pending():
        lines = g.readlines()
        for proc, line in lines:
            yield line


def stream_response(request):
    ip = request.GET.get('ip', '')
    if not ip:
        return "no ip."
    return StreamingHttpResponse(stream_response_generator(ip))


def index(request):
    return HttpResponse(content="""
    <head><style>
    body {
    background: lightblue;
    }
    </style></head>
    <p>Hello

<script>
var xhr = new XMLHttpRequest();
xhr.open('GET', '/tools/test');
xhr.seenBytes = 0;
xhr.onreadystatechange = function() {
  console.log("state change.. state: "+ xhr.readyState);
  if(xhr.readyState == 3) {
    var newData = xhr.response.substr(xhr.seenBytes);
    console.log("newData: <<" +newData+ ">>");
    document.body.innerHTML += "" +newData+ "<br />";
    xhr.seenBytes = xhr.responseText.length;
    console.log("seenBytes: " +xhr.seenBytes);
  }
};
xhr.addEventListener("error", function(e) {
  console.log("error: " +e);
});
console.log(xhr);
xhr.send();
</script>""")
