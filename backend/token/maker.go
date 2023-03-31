package token

import (
	"fmt"
	"time"
)

var(
	ErrTokenExpired=fmt.Errorf("Token has expired")
	ErrBrokenToken=fmt.Errorf("Broken token")
)
type Maker interface{
	CreateToken(email string, duration time.Duration)(string,error)
	VerifyToken(string)(Payload,error)
}