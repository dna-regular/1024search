package main

import (
    "fmt"
    "bytes"
    "net/http"
    "github.com/xfxdev/xlog"
)

func LogInit() {
    strLogLevel := "INFO"  // also maybe read from config.
    logLevel, suc := xlog.ParseLevel(strLogLevel)
    if suc == false {
        // failed to parse log level, will use the default level[INFO] instead."
    }
    xlog.SetLevel(logLevel)
    xlog.SetLayout("%L %f(%i)$ %l")
}

func main() {
    xlog.Info("client start...")
    resp, err := http.Get("http://t66y.com/thread0806.php?fid=7&search=&page=0")
	if err != nil {
        xlog.Error("get error")
		return
	}
    headers := resp.Header
    for k, v := range headers {
		fmt.Printf("k=%v, v=%v\n", k, v)
	}
    defer resp.Body.Close()
    buf := bytes.NewBuffer(make([]byte, 0, 512))
	length, _ := buf.ReadFrom(resp.Body)
	fmt.Println(len(buf.Bytes()))
	fmt.Println(length)
	fmt.Println(string(buf.Bytes()))
}
