package db

import (
	"context"
	"database/sql"
	"fmt"
	"time"
	"math"
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
func (model *SQLModel)execTx(ctx context.Context,fn func (q *Queries)error)error{
	tx,err:=model.db.BeginTx(ctx,nil)
	if err!=nil{
		return err
	}
	q:=New(tx)
	err=fn(q)
	if err!=nil{
		rbErr:=tx.Rollback()
		if rbErr!=nil{
			return fmt.Errorf("Transaction Err: %s, Rollback Err: %s",err.Error(),rbErr.Error())
		}
		return fmt.Errorf("Transaction error: %s",err.Error())
	}
	return tx.Commit()
}
type RegisterLockerParam struct{
	UserEmail string
	LockerID int64
}
func (model *SQLModel)RegisterLockerTx(ctx context.Context,param RegisterLockerParam)error{
	err:=model.execTx(ctx,func(q *Queries) error {
		usr,err:=q.GetCustomerByEmail(ctx,param.UserEmail)
		if err!=nil{
			return err
		}
		locker,err:=q.GetCabinetForRent(ctx,param.LockerID)
		if err!=nil{
			return err
		}
		if locker.Avail==false{
			if locker.Userid.Int64==usr.ID{
				return fmt.Errorf("You have registered this locker")
			}
			return fmt.Errorf("The locker has been registered, please choose another one")
		}
		
		err=q.RentCabinet(ctx,RentCabinetParams{
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

const(
	Card string = "card"
	Momo string = "momo"
	Zalo string = "zalopay"
)
type PaymentTxParam struct{
	UserEmail string
	LockerId int64
	Method string
}

func (model *SQLModel)LockerPaymentTx(ctx context.Context, param PaymentTxParam)(CabinetLockerRental,error){
	// var receipt CabinetLockerRental
	var receipt CabinetLockerRental
	err:=model.execTx(ctx,func(q *Queries) error {
		//get user
		usr,err:=q.GetCustomerByEmail(ctx,param.UserEmail)
		if err!=nil{
			return err
		}
		
		//check if locker rent by user
		locker,err:=q.GetCabinetByID(ctx,param.LockerId)
		if err!=nil{
			return err
		}
		if !locker.Userid.Valid || locker.Userid.Int64!=usr.ID{
			return fmt.Errorf("You can only pay locker that you registerd")
		}

		//unrent locker
		

		err=q.UnrentCabinet(ctx,param.LockerId)
		if err!=nil{
			return err
		}


		//create receipt
		receipt,err=q.CreateCabinetRental(ctx,CreateCabinetRentalParams{
			Cabinetid: param.LockerId,
			Customerid: usr.ID,
			Rentdate: locker.Start.Time,
			Duration: fmt.Sprint(math.Ceil(time.Since(locker.Start.Time).Seconds())),
			Paymentmethod: string(param.Method),
			Fee:float64(15000*int64(math.Ceil(time.Since(locker.Start.Time).Hours()))),
		})
		return err
	})
	return receipt,err
}