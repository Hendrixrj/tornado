# notes
a porta default 8080 para ficar em listenner na aplicação web

# comandos
    * git commit -am "new notes"
    * git push
    * fury create-version 0.0.n # (fazer na raiz do projeto)
        (pode ser pedido a senha do fury)

# no site fury.ml.com
create scope associate with version
see deploy of scope in "In Progress section"
validate version /version

create BigQ topics
create BiqQ consumers :
	- associate with version of application, 
	- associate with topic, 
	- define endpoint or path (in post method) for BigQ topic notify consumer when a message arrive, and this consume message and return 200 (ACK)

	Subtask for BigConsumer: 
		create BiqQ Scope :	

			- create a scope analog a application scope, this scope build a infrasctruture for BigQueue, define name of scope, version of application, etc..
			- this scope url will be used for acess operations (post, delete, read, etc) in BigQueue, example : mybigscope.myappname.melifrontends.com/<operation>

