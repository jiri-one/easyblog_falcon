import bcrypt
password = b"super secret password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
if bcrypt.checkpw(password, hashed):
	print("It Matches!")
	hashed = bcrypt.hashpw(password, bcrypt.gensalt())
else:
	print("It Does not Match :(")

print(hashed)
# zahashuj jak heslo, tak i jmeno!!!! v budoucnu zahashuj i email
# připrav si databazi a k ni script pro pridavani uzivatelu do databaze