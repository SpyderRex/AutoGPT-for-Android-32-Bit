from revChatGPT.V1 import Chatbot
GPT = Chatbot(config={
  "access_token": r"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJsdXRocGhhbGhhcXVlQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLVFjSEs3VU5GcUhXQ0gySTNHZXkxWHN0aiJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMzMTMyNDgzMTI5OTIwODA1MjEiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjkwNTMxNjA0LCJleHAiOjE2OTE3NDEyMDQsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.Pl8ixBBgL0xJBOwxYevdA-DNBYWrOtjtraz6kq3LVtsozimQCDjN8GqRmiS95bVIpjKftEjYfVTE0Dk-d8Ja9ABiHMBWpSk7uPE93RC-SkC2SmALTWkqs6BRD7Yp83MCdGFva0Pvre1qFWfw1qx2djt_qGzTP8Cbq2icCOm-L301nnmsQmMNd98KIxS8-B2v-FJ0t8PHHSfD-waqkBnMEw4arr524BjUclLUdWnCANFbiw0Mr2lqzj-Up3BqtwfO1m_UwL68t4WidJ1BeBXmWZeudEmi8vEIjT_O9eZCPmJeeswgle8GEr7Y-sLC3Vs4oCpPBciTXiPfT-RBAJo9_A"
  })
while True:
	for token in GPT.ask(input("Enter your prompt:")):
                    message = token["message"][len(prev_text) :]
                    print(message, end="", flush=True)
                    prev_text = token["message"]
