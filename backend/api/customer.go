package api

import (
	"database/sql"
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
	db "github.com/vutranhoang1411/do_an_da_nganh/db/sqlc"
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
	customer,err:=server.model.CreateCustomer(ctx,arg)
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError(err));
		return
	}

	ctx.JSON(http.StatusOK,customer)
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
		ctx.JSON(http.StatusForbidden,handleError(fmt.Errorf("Wrong username or password!")))
		return
	}
	token,err:=server.maker.CreateToken(reqBody.Email,server.config.TokenDuration)
	if err!=nil{
		ctx.JSON(http.StatusInternalServerError,handleError(err))
	}
	//return some kind of token
	ctx.JSON(http.StatusOK,map[string]string{
		"token":token,
	})
}
func (server *Server) userRegisterLocker(ctx *gin.Context){
	locker_id_param:=ctx.PostForm("locker_id")
	if len(locker_id_param)<1{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("No locker ID provided")))
		return
	}
	lockerID,err:=strconv.ParseInt(locker_id_param,10,64)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("Invalid locker id")))
		return
	}
	user_email:=ctx.GetString("user_info")
	err=server.model.RegisterLockerTx(ctx,db.RegisterLockerParam{
		UserEmail: user_email,
		LockerID: lockerID,
	})
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,err)
		return
	}
	ctx.JSON(http.StatusOK,map[string]string{
		"msg":"Success register locker",
	})
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
	ctx.JSON(http.StatusOK,map[string][]db.Cabinet{
		"locker_list":locker_list,
	})
}

type makePaymentParam struct{
	lockerID int64 `form:"locker_id" binding:"required"`
	paymentMethod db.PaymentMethod `form:"method" binding:"required"`
}
func (server *Server) makePayment(ctx *gin.Context){
	var req makePaymentParam
	err:=ctx.ShouldBind(&req)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	user_email:=ctx.GetString("user_info")
	receipt,err:=server.model.LockerPaymentTx(ctx,db.PaymentTxParam{
		UserEmail: user_email,
		LockerId: req.lockerID,
		Method: req.paymentMethod,
	})
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	ctx.JSON(http.StatusOK,map[string]db.CabinetLockerRental{
		"receipt":receipt,
	})
}
func (server *Server) openLocker(ctx *gin.Context){
	file_header,err:=ctx.FormFile("img")
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(err))
		return
	}
	//init buffer and get the file
	size:=file_header.Size
	buffer:=make([]byte,size)
	file,err:=file_header.Open()
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("upload file error")))
		return
	}
	//read img into buffer
	_,err=file.Read(buffer)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("upload file error")))
		return
	}
	
	//write to destination, for testing purpose
	dest,_:=os.Create("./static/temp/temp.png")
	_,err=dest.Write(buffer)
	if err!=nil{
		ctx.JSON(http.StatusBadRequest,handleError(fmt.Errorf("upload file error")))
		return
	}
	ctx.JSON(http.StatusOK,struct{}{})
	
}