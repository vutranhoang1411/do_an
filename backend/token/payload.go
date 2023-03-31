package token
import (
	"time"

	"github.com/google/uuid"
)
type Payload struct{
	ID uuid.UUID `json:"id"`
	Email string `json:"email"`
	IssuedAt time.Time `json:"issued_at"`
	ExpiredAt time.Time `json:"expired_at"`
}

func NewPayload(email string,duration time.Duration)(Payload,error){
	tokenID,err:=uuid.NewUUID()
	var payload Payload
	if (err!=nil){
		return payload,err
	}
	payload=Payload{
		ID:tokenID,
		Email: email,
		IssuedAt: time.Now(),
		ExpiredAt: time.Now().Add(duration),
	}
	return payload,nil
}
