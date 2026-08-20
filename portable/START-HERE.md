# EA Stödjare – portabel ChatGPT-version

Detta paket gör den aktuella Custom GPT-konfigurationen användbar i en vanlig ChatGPT-konversation.

1. Läs `assistant/instructions.md` först och använd den som arbetsinstruktion för hela konversationen.
2. Använd filerna i `knowledge/` som samma primära Knowledge som i Custom GPT Builder.
3. `supporting/` innehåller maskinläsbara modeller, scheman och mallar som kan användas när uppgiften kräver projektarbete eller validering; de får inte överstyra instruktionen eller Builder Knowledge.
4. Behåll YAML som source of truth för EA-projekt enligt instruktionen och Knowledge-paketet.
5. Om användaren bifogar ett befintligt EA Stödjare-projekt ska dess manifest, modellfiler, revision och källregister behandlas enligt projektets ordinarie integritets- och proveniensregler.

Användarens aktuella instruktioner har alltid företräde framför paketets arbetsregler.
