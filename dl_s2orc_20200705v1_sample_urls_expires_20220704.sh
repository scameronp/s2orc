#!/bin/bash

# create directory
mkdir 20200705v1
mkdir 20200705v1/sample/
mkdir 20200705v1/sample/metadata/
mkdir 20200705v1/sample/pdf_parses/

wget -O 20200705v1/LICENSE 'https://ai2-s2-s2orc.s3.amazonaws.com/20200705v1/LICENSE?AWSAccessKeyId=AKIA5BJLZJPW4OD5EQ2P&Signature=MOvtG8Se8P1qZvr3sf6LzBF3cJI%3D&Expires=1656966980'

wget -O 20200705v1/RELEASE_NOTES 'https://ai2-s2-s2orc.s3.amazonaws.com/20200705v1/RELEASE_NOTES?AWSAccessKeyId=AKIA5BJLZJPW4OD5EQ2P&Signature=Y%2FjdbcRAxmuSr9Gy7RhBqs06kL4%3D&Expires=1656966980'

wget -O 20200705v1/sample/metadata/sample.jsonl 'https://ai2-s2-s2orc.s3.amazonaws.com/20200705v1/sample/metadata/sample.jsonl?AWSAccessKeyId=AKIA5BJLZJPW4OD5EQ2P&Signature=FAEWORtjnNxzbLdENuncwgP7vbw%3D&Expires=1656966980'

wget -O 20200705v1/sample/pdf_parses/sample.jsonl 'https://ai2-s2-s2orc.s3.amazonaws.com/20200705v1/sample/pdf_parses/sample.jsonl?AWSAccessKeyId=AKIA5BJLZJPW4OD5EQ2P&Signature=93rLsMbAwShUOdIXJBfzju196%2B4%3D&Expires=1656966980'

