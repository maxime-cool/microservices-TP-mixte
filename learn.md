GraphQL:
优点：只返回需要的数据；没有入口点数目的乘法；不用添加入口点，灵活添加资源
缺点： 因为每个请求不同，缓存更困难

基本原理：
用户端： HTTP/1.1 POST方法； 来自单一入口点的HTTP请求； body = request GraphQL
服务器端： 接受请求（Reception de la requete）； 解决请求； 发送响应reponse

API GraphQL - 模式
scheme模式内容：
object types
fields: 上面object types的内容
Type scalaires - > 指定类型int, float, string

操作类型 Operation Type
GraphQL 的操作类型可以是 query、mutation 或 subscription，描述客户端希望进行什么样的操作

query 查询：获取数据，比如查找，CRUD 中的 R
mutation 变更：对数据进行变更，比如增加、删除、修改，CRUD 中的 CUD
substription 订阅：当数据发生更改，进行消息推送

// scheme example
type Query{
    get_user_byid(_id:String!): User
    get_user_booking_movies(_id:String!): Movie
}

type User{

}

{
    "data": {
        "hero": {
            name: "V"
        }
        "droid": {
            name: "B'
        }
    }
}

query{
  movie_with_id(_id:"96798c08-d19b-4986-a05d-7da856efb697") {
    id
    title
    rating
    director
  }
}

query{
    user(_id:"alice"){
        name
        brithday
    }
}

{
    "data":{
        "user":{
            "name": Alice
            "brithday" : "2000"
        }
    }
}

