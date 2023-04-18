package util

import (
    "crypto/sha1"
    "encoding/base64"
)

func GetHashedImg(str string)string {
    hasher := sha1.New()
    hasher.Write([]byte(str))
    return base64.URLEncoding.EncodeToString(hasher.Sum(nil))
}