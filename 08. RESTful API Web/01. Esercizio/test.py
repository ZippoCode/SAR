from requests import post, get, put, delete

if __name__ == '__main__':

    request_post = post("http://localhost:8080/api/v0.1/color/red", json={'r': 254, 'g': 200, 'b': 119})
    print(request_post.json())
    print(request_post.status_code)

    request_get = get("http://localhost:8080/api/v0.1/color/red")
    print(request_get.json())
    print(request_get.status_code)

    request_put = put("http://localhost:8080/api/v0.1/color/green", json={'r': 12, 'g': 13, 'b': 29})
    print(request_put.json())
    print(request_put.status_code)

    # request_delete = delete("http://localhost:8080/api/v0.1/color/green")
    # print(request_delete.status_code)
