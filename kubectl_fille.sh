kubectl get nodes
deploymentYaml=$(cat <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
  labels:
	app: fastapi
spec:
  replicas: 1
  selector:
	matchLabels:
	  app: fastapi
  template:
	metadata:
	  labels:
		app: fastapi
	spec:
	  containers:
	  - name: fastapi
		image: $1/$2:$3
		ports:
		- containerPort: 8000
EOF
)


serviceYaml=$(cat <<EOF
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
	app: fastapi
  ports:
	- protocol: TCP
	  port: 8000
	  targetPort: 8000
  type: LoadBalancer
EOF
)
if [ -e deployment.yml ]
then
	rm -rf deployment.yml
fi
if [ -e service.yml ]
then
	rm -rf service.yml
fi

echo "$deploymentYaml" > deployment.yml
echo "$serviceYaml" > service.yml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
sleep 50
kubectl destroy

