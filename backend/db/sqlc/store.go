package db

import (
	"context"
	"database/sql"
	"fmt"
	"time"
)

type Model interface{
	Querier
	RegisterLockerTx(ctx context.Context,param RegisterLockerParam)error
	LockerPaymentTx(ctx context.Context, param PaymentTxParam)(CabinetLockerRental,error)
}

type SQLModel struct{
	*Queries
	db *sql.DB
}

func NewModel(db *sql.DB)Model{
	return &SQLModel{
		Queries: New(db),
		db:db,
	}
}
func (model *SQLModel)execTx(ctx context.Context,fn func (q *Queries,txCtx context.Context)error)error{
	tx,err:=model.db.BeginTx(ctx,nil)
	if err!=nil{
		return err
	}
	q:=New(tx)
	err=fn(q,ctx)
	if err!=nil{
		if rbErr:=tx.Rollback();rbErr!=nil{
			return fmt.Errorf("Transaction Err:%s, Rollback Err:%s",err.Error(),rbErr.Error())
		}
		return err
	}
	return tx.Commit()
}
type RegisterLockerParam struct{
	UserEmail string
	LockerID int64
}
func (model *SQLModel)RegisterLockerTx(ctx context.Context,param RegisterLockerParam)error{
	err:=model.execTx(ctx,func(q *Queries,txCtx context.Context) error {
		usr,err:=model.GetCustomerByEmail(txCtx,param.UserEmail)
		if err!=nil{
			return err
		}
		locker,err:=model.GetCabinetForRent(txCtx,param.LockerID)
		if err!=nil{
			return err
		}
		if locker.Avail==false{
			return fmt.Errorf("The locker has been registered, please choose another one")
		}
		
		err=model.RentCabinet(txCtx,RentCabinetParams{
			Userid: sql.NullInt64{
				Int64: usr.ID,
				Valid: true,
			},
			ID: param.LockerID,
		})
		return err
	})
	return err
}
type PaymentMethod string
const(
	Card PaymentMethod = "card"
	Momo PaymentMethod = "momo"
	Zalo PaymentMethod = "zalopay"
)
type PaymentTxParam struct{
	UserEmail string
	LockerId int64
	Method PaymentMethod
}

func (model *SQLModel)LockerPaymentTx(ctx context.Context, param PaymentTxParam)(CabinetLockerRental,error){
	var receipt CabinetLockerRental
	err:=model.execTx(ctx,func(q *Queries, txCtx context.Context) error {
		//get user
		usr,err:=model.GetCustomerByEmail(txCtx,param.UserEmail)
		if err!=nil{
			return err
		}
		
		//check if locker rent by user
		locker,err:=model.GetCabinetByID(txCtx,param.LockerId)
		if err!=nil{
			return err
		}
		if !locker.Userid.Valid || locker.Userid.Int64!=usr.ID{
			return fmt.Errorf("You can only pay locker that you registerd")
		}

		//unrent locker
		err=model.UnrentCabinet(ctx,param.LockerId)
		if err!=nil{
			return err
		}
		//create receipt
		receipt,err=model.CreateCabinetRental(ctx,CreateCabinetRentalParams{
			Cabinetid: param.LockerId,
			Customerid: usr.ID,
			Rentdate: locker.Start.Time,
			Duration: int64(time.Since(locker.Start.Time)),
			Paymentmethod: string(param.Method),
			Fee:"teting fee amount",
		})
		return err
	})
	return receipt,err
}