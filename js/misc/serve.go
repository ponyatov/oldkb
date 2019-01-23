package main

import (
	"log"
	"net/http"
	"os"
)

const HTTP = ":11111"

func main() {
	log.Println(os.Args)
	log.Println(HTTP)
	http.Handle("/", http.FileServer(http.Dir(".")))
	log.Fatal(http.ListenAndServe(HTTP, nil))
}
