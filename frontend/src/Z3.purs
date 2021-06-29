module Z3 where

import Prelude
import Data.Maybe
import Data.Either (Either(..))
import Affjax as AX
import Affjax.ResponseFormat as ResponseFormat
import Data.Argonaut.Core (stringify, fromString, Json)
import Effect.Class.Console (log)
import Affjax.RequestBody as RequestBody
import Effect.Aff (launchAff_)

--simplify given expression exp
simplifyExp :: String->String --Strings should be Exp
simplifyExp expression = returned
    where returned = sendRequest "http://blum.cs.haverford.edu:8080/simplify" "{'test':'hello'}"

--see if equation or inequality is correct given exp and assumptions
checkExp :: String->Boolean --note that String parameter should be Exp
checkExp expression = returned
    where returned = sendRequest "http://blum.cs.haverford.edu:8080/checker" "{'test':'hello'}"

sendRequest :: String String -> Json --probably not the right types
sendRequest url body = launchAff_ do 
    result2 <- AX.post ResponseFormat.json url (Just (RequestBody.json (fromString body)))
    case result2 of
        Left err -> log $ "POST" <> url <> "response failed to decode: " <> AX.printError err
        Right response -> log $ "POST" <> url <> "response: " <> stringify response.body