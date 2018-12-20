package main

import (
    "net/http"
    "log"
)


func main() {
	log.println("")
	http.ListenAndServe(":9090", nil)
}

