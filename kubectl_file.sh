kubectl get nodes
deploymentYaml=$(cat <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apis-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: apis-service
  template:
    metadata:
      labels:
        app: apis-service
    spec:
      nodeSelector:
        "kubernetes.io/os": linux
      containers:
      - name: order-service
	image: $1/$2:$3
        ports:
        - containerPort: 8000
EOF
)


serviceYaml=$(cat <<EOF
apiVersion: v1
kind: Service
metadata:
  name: apis-service
spec:
  type: LoadBalancer
  ports:
  - name: http
    port: 80
    targetPort: 8000
  selector:
    app: apis-service
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

