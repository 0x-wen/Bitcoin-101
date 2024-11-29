## bitcoin地址生成与解析
[膜拜大佬笔记](https://aandds.com/blog/bitcoin-key-addr.html#org0000001)

### p2pkh 推导过程

![img.png](../picture/img.png)

- 传入一个公钥解析，02，03开头的是压缩公钥，其他类型为非压缩公钥
- ripemd160(sha256(b)), 先将公钥进行sha256，再进行ripemd160
![img.png](../picture/img1.png)
- 计算checksum, 主网PubKeyHashAddrID: 0x00,测试网:TestNetAddrID: 0x6f, 进行两次sha256，取前4位
```go
h := sha256.Sum256(input)
h2 := sha256.Sum256(h[:])
copy(cksum[:], h2[:4])
```
- [version + ripemd160_hash + checksum] 的切片数据，然后使用base58编码

## 解锁脚本 与 锁定脚本
通过地址 即可得到 锁定脚本，用于给接受方
解锁脚本 用于发送方，需要signatureScript和publicKey

### 隔离见证
通过提取signatureScript,将数据放在witness中，确保了交易的延展性
之前的标准地址，signatureScript根据ecdsa的签名算法，会出现(x,y)和(x,-y)同时签名一个utxo，从而导致txid不确定


## taproot
[taproot总结](https://aandds.com/blog/bitcoin-taproot.html)