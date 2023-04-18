package token

import (
	"time"

	"github.com/o1egl/paseto"
)

type PasetoMaker struct{
	paseto *paseto.V2
	symmetrickey []byte
}

func NewPasetoMaker(symmetrickey string)Maker{
	return &PasetoMaker{
		paseto: paseto.NewV2(),
		symmetrickey: []byte(symmetrickey),
	}
}

func (maker *PasetoMaker)CreateToken(email string, duration time.Duration)(string,error){
	payload,err:=NewPayload(email,duration)
	if err!=nil{
		return "",err
	}
	token,err:=maker.paseto.Encrypt(maker.symmetrickey,payload,nil)
	if err!=nil{
		return "",err
	}
	return token,nil

}
func (maker *PasetoMaker)VerifyToken(token string)(Payload,error){
	var payload Payload
	err:=maker.paseto.Decrypt(token,maker.symmetrickey,&payload,nil)
	if err!=nil{
		return payload,ErrBrokenToken
	}
	if payload.ExpiredAt.Before(time.Now()){ //expired token
		return payload,ErrTokenExpired
	}
	return payload,nil
}