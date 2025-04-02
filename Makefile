.PHONY: up down

##########
# DOCKER #
##########

SERVICES := backend

# start services
up:
	@make down && docker compose -p papernest up --build --force-recreate $(SERVICES) -d
down:
	@docker compose -p papernest down
