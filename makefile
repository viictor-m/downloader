dir     = $(shell pwd)
raiz    = $(shell dirname $(dir))
projeto = $(shell basename $(dir))

# caso seja de interesse buildar a imagem a partir de um dockerfile particular
# https://docs.docker.com/engine/reference/commandline/build/#specify-a-dockerfile--f
dockerfile = dockerfile

# sobrescreva diretamente na linha de comando para alterar. Exemplo:
# make -C scripts/ -f aws.mk criar-repositorio regiao=us-east-2 perfil=prod
regiao  = us-east-1
perfil  = dev
id      = $(shell aws sts get-caller-identity --output json --profile ${perfil} | jq '.Account' | sed 's/\"//g')

python/instalar-ambiente:
	@echo "INFO: instalando ambiente '$(dir)'"
	@conda env create -f requirements.yaml

python/ativar-ambiente:
	@echo "INFO: ativando projeto '$(dir)'"
	@conda activate $(dir)


python/formatar-codigo:
	@echo "INFO: executando Autoflake8"
	@conda run -n $(projeto) autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src tests --exclude=__init__.py

	@echo "INFO: executando Black"
	@conda run -n $(projeto) black src tests

	@echo "INFO: executando Isort"
	@conda run -n $(projeto) isort src tests

python/checar-codigo:
	@echo "INFO: verificando com Flake8"
	@conda run -n $(projeto) flake8 src tests

	@echo "INFO: verificando com Pydocstyle"
	@conda run -n $(projeto) pydocstyle src

	@echo "INFO: verificando com Mypy"
	@conda run -n $(projeto) mypy src

python/gerar-requirements: python/ativar-ambiente
	@echo "INFO: gerando requirements do projeto '$(dir)'"
	@conda env export --no-builds -n $(projeto) |\
		grep -v "^prefix:" > "requirements.yaml"

docker/limpar-tudo:
	@echo "INFO: todas as imagens e containers serão removidos"
	@docker system prune -a

docker/buildar: python/gerar-requirements
	@echo "INFO: iniciando build para '$(dir)/$(dockerfile)'"
	@docker build -t $(projeto) -f $(dir)/$(dockerfile) $(dir)

aws/ecr/criar-repositorio:
	@aws ecr create-repository \
		--registry-id $(id) \
		--repository-name $(projeto) \
		--profile $(perfil) > /dev/null || \
		echo "a criação do repositório falhou. '$(projeto)' existe?"

aws/ecr/remover-repositorio:
	@aws ecr delete-repository \
		--registry-id $(id) \
		--repository-name $(projeto) \
		--profile $(perfil) > /dev/null || \
		echo "a remoção do repositório falhou. '$(projeto)' existe?"

aws/ecr/atualizar-repositorio: aws/ecr/criar-repositorio docker/buildar
	@echo "INFO: autenticando AWS | perfil '$(perfil)' | conta '$(id)'"
	@aws ecr get-login-password \
		--region $(regiao) \
		--profile $(perfil) | docker login --username AWS \
		--password-stdin $(id).dkr.ecr.$(regiao).amazonaws.com
	@docker tag $(projeto):latest \
		$(id).dkr.ecr.$(regiao).amazonaws.com/$(projeto):latest
	@echo "INFO: iniciando upload da imagem para o ECR"
	@docker push $(id).dkr.ecr.$(regiao).amazonaws.com/$(projeto):latest


# https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html
aws/lambda/criar-funcao:
	@echo "ainda não implementado"

aws/lambda/atualizar-imagem: aws/ecr/criar-repositorio
	@echo "INFO: a função '$(projeto)' terá a imagem atualizada"
	@aws lambda update-function-code \
		--region $(regiao) \
		--function-name $(projeto) \
		--image-uri $(id).dkr.ecr.$(regiao).amazonaws.com/$(projeto):latest \
		--profile $(perfil) > /dev/null || \
		echo "a atualização da lambda '$(projeto)' falhou. A função existe?"

aws/sam/executar-lambda-localmente: python/gerar-requirements
	@echo "INFO: a lambda será ativada com o evento '$(evento)'"
	@sam build -t .aws/lambda/template.yaml
	@sam local invoke -e .aws/lambda/eventos/$(evento).json --profile $(perfil)
	@rm requirements.txt

