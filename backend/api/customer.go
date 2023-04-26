package api

import (
	"database/sql"
	"fmt"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	db "github.com/vutranhoang1411/do_an_da_nganh/db/sqlc"
	"github.com/vutranhoang1411/do_an_da_nganh/util"
)
type createUserRequest struct{
	Name     string `json:"name" form:"name" binding:"required"`
	Email    string `json:"email" form:"email" binding:"required,email"`
	Password string `json:"password" form:"password" binding:"required,min=8"`
}
func (server *Server) createUser(ctx *gin.Context){
	var reqBody createUserRequest;
	if err:=ctx.ShouldBind(&reqBody);err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	// password,err:=util.HashPassword(reqBody.Password);
	// if (err!=nil){
	// 	ctx.JSON(http.StatusInternalServerError,handleError(err));
	// 	return
	// }
	arg:=db.CreateCustomerParams{
		Name: reqBody.Name,
		Email: reqBody.Email,
		Password: reqBody.Password,
	}
	_,err:=server.model.CreateCustomer(ctx,arg)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err));
		return
	}

	ctx.JSON(http.StatusOK,map[string]any{})
}
type loginUserRequest struct{
	Email    string `json:"email" form:"email" binding:"required,email"`
	Password string `json:"password" form:"password" binding:"required,min=8"`
}
func (server *Server) loginUser(ctx *gin.Context){
	var reqBody loginUserRequest
	if err:=ctx.ShouldBind(&reqBody);err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	customer,err:=server.model.GetCustomerByEmail(ctx,reqBody.Email)
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError((err)))
		return
	}
	if reqBody.Password!=customer.Password{
		ctx.JSON(http.StatusForbidden,handleError(fmt.Errorf("wrong username or password")))
		return
	}
	token,err:=server.maker.CreateToken(reqBody.Email,server.config.TokenDuration)
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError(err))
		return
	}
	//return some kind of token
	ctx.JSON(http.StatusOK,map[string]string{
		"token":token,
	})
}
type userRegisterLockerRequest struct{
	LockerID int64 `json:"locker_id"`
}
func (server *Server) userRegisterLocker(ctx *gin.Context){
	var req userRegisterLockerRequest
	err:=ctx.ShouldBindJSON(&req)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("no locker ID provided")))
		return
	}
	user_email:=ctx.GetString("user_info")
	usr,err:=server.model.GetCustomerByEmail(ctx,user_email)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	if !usr.Photo.Valid{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("You must post your avatar before register")))
		return
	}
	err=server.model.RegisterLockerTx(ctx,db.RegisterLockerParam{
		UserEmail: user_email,
		LockerID: req.LockerID,
	})
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	ctx.JSON(http.StatusOK,map[string]string{
		"msg":"Success register locker",
	})
}
type GetLockerResponse struct{
	ID int64 `json:"id"`
	Start string `json:"start_time"`
	Open bool `json:"open"`
}
func (server *Server) getUserLocker(ctx *gin.Context){
	user_email:=ctx.GetString("user_info")
	usr,err:=server.model.GetCustomerByEmail(ctx,user_email)
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError(err))
		return
	}
	locker_list,err:=server.model.GetUserCabinet(ctx,sql.NullInt64{
		Int64: usr.ID,
		Valid: true,
	})
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError(err))
		return
	}
	res:=[]GetLockerResponse{}
	for _,locker:=range locker_list{
		temp:=GetLockerResponse{
			ID:locker.ID,
			Open: locker.Open,
		}
		if locker.Start.Valid{
			temp.Start=locker.Start.Time.Format("2006-01-02 15:04:05")
		}else{
			temp.Start=""
		}
		res=append(res, temp)
	}
	ctx.JSON(http.StatusOK,res)
}

type makePaymentParam struct{
	LockerID int64 `json:"locker_id" form:"locker_id" binding:"required"`
	PaymentMethod string `json:"method" form:"method"`
}
func (server *Server) makePayment(ctx *gin.Context){
	var req makePaymentParam
	err:=ctx.ShouldBind(&req)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	if req.PaymentMethod!=db.Card&&req.PaymentMethod!=db.Momo&&req.PaymentMethod!=db.Zalo{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("invalid payment method: %s",req.PaymentMethod)))
		return
	}
	user_email:=ctx.GetString("user_info")
	receipt,err:=server.model.LockerPaymentTx(ctx,db.PaymentTxParam{
		UserEmail: user_email,
		LockerId: req.LockerID,
		Method: req.PaymentMethod,
	})
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	ctx.JSON(http.StatusOK,receipt)
}
func (server *Server) updateImg(ctx *gin.Context){
	//get file from post form
	user_email:=ctx.GetString("user_info")
	file_header,err:=ctx.FormFile("img")
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	//init buffer and read the file
	size:=file_header.Size
	buffer:=make([]byte,size)
	file,err:=file_header.Open()
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("upload file error")))
		return
	}
	_,err=file.Read(buffer)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("upload file error")))
		return
	}

	//create file
	hash_name:=util.GetHashedImg(user_email)+".jpg"
	err=os.WriteFile("./public/img/"+hash_name,buffer,0644)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}

	//update to database
	err=server.model.UpdateUserPhoto(ctx,db.UpdateUserPhotoParams{
		Photo: sql.NullString{
			String: hash_name,
			Valid: true,
		},
		Email: user_email,
	})
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	ctx.JSON(http.StatusOK,map[string]string{
		"msg":"Success",
	})

}

	
// 	//write to destination, for testing purpose
// 	dest,_:=os.Create("./static/temp/temp.png")
// 	_,err=dest.Write(buffer)
// 	if err!=nil{
// 		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("upload file error")))
// 		return
// 	}
// 	ctx.JSON(http.StatusOK,struct{}{})
	
// }