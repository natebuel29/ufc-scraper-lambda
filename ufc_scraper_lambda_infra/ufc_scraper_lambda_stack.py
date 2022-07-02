from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    aws_iam as iam,
    App, Duration, Stack, RemovalPolicy
)


class UfcScraperLambdaInfraStack(Stack):

    def __init__(self, app: App, id: str) -> None:
        super().__init__(app, id)

        # create layer
        layer = lambda_.LayerVersion(self, 'scrapy',
                                     code=lambda_.Code.from_asset("layer"),
                                     description='Scrapy layer',
                                     compatible_runtimes=[
                                         lambda_.Runtime.PYTHON_3_6,
                                         lambda_.Runtime.PYTHON_3_7,
                                         lambda_.Runtime.PYTHON_3_8
                                     ],
                                     removal_policy=RemovalPolicy.DESTROY
                                     )

        lambdaFn = lambda_.Function(
            self, "UfcFutureFightLambda",
            code=lambda_.Code.from_asset("src"),
            handler="index.handler",
            timeout=Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_8,
            layers=[layer]
        )

        # Run every day at 6PM UTC
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='22',
                hour='2',
                month='*',
                week_day='MON-SAT',
                year='*'),
        )

        rule.add_target(targets.LambdaFunction(lambdaFn))

        getSecretPolicy = iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"], resources=["arn:aws:secretsmanager:*"])

        lambdaFn.role.attach_inline_policy(iam.Policy(
            self, "ufc-scraper-lambda-policy", statements=[getSecretPolicy]))
