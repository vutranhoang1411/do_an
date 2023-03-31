CREATE TABLE cabinet
(
  ID    bigserial  NOT NULL,
  avail   bool NOT NULL DEFAULT true,
  open   bool NOT NULL DEFAULT false,
  start  timestamp,
  userID bigint ,
  PRIMARY KEY (ID)
);


CREATE TABLE cabinet_locker_rentals
(
  ID            bigserial    NOT NULL,
  CabinetID     bigint       NOT NULL,
  CustomerID    bigint       NOT NULL,
  rentdate      timestamp not null,
  duration      interval  NOT NULL,
  paymentMethod varchar      NOT NULL,
  fee           decimal   NOT NULL,
  PRIMARY KEY (ID)
);



CREATE TABLE customer
(
  ID          bigserial     NOT NULL,
  name        varchar NOT NULL,
  email         varchar not null unique,
  password      varchar not null,
  photo         VARCHAR,
  PRIMARY KEY (ID)
);


ALTER TABLE cabinet_locker_rentals
  ADD CONSTRAINT FK_customer_TO_Cabinet_Locker_Rentals
    FOREIGN KEY (CustomerID)
    REFERENCES customer (ID);

ALTER TABLE cabinet_locker_rentals
  ADD CONSTRAINT FK_Cabinet_TO_Cabinet_Locker_Rentals
    FOREIGN KEY (CabinetID)
    REFERENCES cabinet (ID);

ALTER TABLE cabinet
  ADD CONSTRAINT FK_customer_TO_Cabinet
    FOREIGN KEY (userID)
    REFERENCES customer (ID);