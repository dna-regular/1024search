package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/xfxdev/xlog"
)

func LogInit() {
	strLogLevel := "INFO" // also maybe read from config.
	logLevel, suc := xlog.ParseLevel(strLogLevel)
	if suc == false {
		// failed to parse log level, will use the default level[INFO] instead."
	}
	xlog.SetLevel(logLevel)
	xlog.SetLayout("%L %f(%i)$ %l")
}

func http_get(url string) string {
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		xlog.Error("create req err: ", err)
		return ""
	}
	req.Header.Add("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
	resp, err := client.Do(req)
	if err != nil {
		xlog.Error("get error: ", err)
		return ""
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		xlog.Error("get error: ", url, resp.StatusCode)
		return ""
	}

	buf := bytes.NewBuffer(make([]byte, 0, 1024*1024*2))
	buf.ReadFrom(resp.Body)
	return string(buf.Bytes())
}

func do_search(keyword string) []string {
	urls := make([]string, 0, 100)
	for i := 0; i < 100; i++ {
		url := "http://t66y.com/thread0806.php?fid=7&search=&page=" + strconv.Itoa(i)
		resp := http_get(url)
		if strings.Contains(resp, keyword) {
			fmt.Println(url)
			urls = append(urls, url)
		}
		fmt.Printf("\r%d %s", i, url)
	}
	return urls
}

func main() {
	LogInit()
	xlog.Info("client start...")
	if len(os.Args) != 2 {
		print("usage:\n")
		print("\t./search <keyward>\n")
		return
	}
	urls := do_search(os.Args[1])
	for url := range urls {
		print(url)
	}
}
