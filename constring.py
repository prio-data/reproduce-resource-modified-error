from functools import partial
connection_string = lambda protocol, host, port, account_name, account_key: (
    f"DefaultEndpointsProtocol={protocol};"
    f"AccountName={account_name};"
    f"AccountKey={account_key};"
    f"BlobEndpoint=http://{host}:{port}/{account_name};"
    )

vanilla_connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1")

testing_connection_string = partial(connection_string, "http", "127.0.0.1", "10000", "pedlan@prio.org", "letmein")
