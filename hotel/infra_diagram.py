from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.saas.cdn import Cloudflare
from diagrams.custom import Custom

with Diagram("Hotel Reservation System", show=True):
    user = Cloudflare("User")

    with Cluster("Render"):
        render_web = Custom("Flask App", "./render.png")
        db = RDS("Database")

    with Cluster("CI/CD"):
        github = Github("GitHub")
        actions = GithubActions("GitHub Actions")
        docker = Docker("Docker Compose")

    user >> ELB("Load Balancer") >> render_web
    render_web >> db

    github >> actions >> docker >> render_web
    docker >> db