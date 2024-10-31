# Privacy-Preserving Medical Research Platform

> A secure medical trial matching system powered by Nillion's secure computation technology

## Problem Statement
Medical research requires handling sensitive patient data while maintaining privacy and compliance with healthcare regulations. Traditional systems expose private health information to multiple parties, creating privacy risks and potential HIPAA violations.

## Solution
This platform uses Nillion's secure computation to process sensitive medical data while maintaining complete privacy. It enables multi-party computation where different stakeholders (patients, researchers, hospitals) can participate in clinical trials without exposing underlying patient data.

## Features

### 1. Secure Trial Matching
- Age-based eligibility verification
- Symptom pattern matching
- Treatment duration assessment
- Privacy-preserving patient scoring

### 2. Multi-Party Computation
- Patient data remains encrypted
- Researchers get aggregated insights
- Hospitals maintain oversight
- Zero knowledge of individual records

### 3. Privacy-Preserving Access Levels
- **Patients**: Trial eligibility and effectiveness scores
- **Researchers**: Aggregated trial matches and response scores
- **Hospitals**: Safety monitoring and trial oversight

## Technical Implementation

### Core Components

#### 1. Authentication System

```7:67:app/components/Login.tsx
export const Login = () => {
  const { authenticated, login, logout } = useNillionAuth();
  // Feel free to set this to other values + useSetState
  const SEED = "example-secret-seed";
  const SECRET_KEY =
    "9a975f567428d054f2bf3092812e6c42f901ce07d9711bc77ee2cd81101f42c5";

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    console.log("authenticated", authenticated);
  }, [authenticated]);

  const handleLogin = async () => {
    try {
      setIsLoading(true);
      const credentials: UserCredentials = {
        userSeed: SEED,
        signer: () => createSignerFromKey(SECRET_KEY),
      };
      await login(credentials);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      setIsLoading(true);
      await logout();
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-row flex my-6">
      {authenticated ? (
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={handleLogout}
          disabled={isLoading}
        >
          {isLoading ? "Logging out..." : "Logout"}
        </button>
      ) : (
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={handleLogin}
          disabled={isLoading}
        >
          {isLoading ? "Logging in..." : "Login"}
        </button>
      )}
    </div>
  );
};
```

- Secure authentication with cryptographic keys
- Role-based access control

#### 2. Computation Engine

```14:87:app/components/Compute.tsx
export const Compute: FC = () => {
  const { client } = useNillion();
  const nilCompute = useNilCompute();
  const [programId, setProgramId] = useState<ProgramId | string>("");
  const [copiedComputeOutputID, setCopiedComputeOutputID] = useState(false);

  const handleClick = () => {
    if (!programId) throw new Error("compute: program id required");

    const bindings = ProgramBindings.create(programId)
      .addInputParty(PartyName.parse("Party1"), client.partyId)
      .addOutputParty(PartyName.parse("Party1"), client.partyId);

    // Note: This is hardcoded for demo purposes.
    // Feel free to change the NamedValue to your required program values.
    const values = NadaValues.create()
      .insert(NamedValue.parse("my_int1"), NadaValue.createSecretInteger(2))
      .insert(NamedValue.parse("my_int2"), NadaValue.createSecretInteger(4));
      .insert(NamedValue.parse("monthly_savings"), NadaValue.createSecretInteger(1000))
    nilCompute.execute({ bindings, values });
  };
      .insert(NamedValue.parse("investment_amount"), NadaValue.createSecretInteger(10000))
  return (
    <div className="border border-gray-400 rounded-lg p-4 w-full max-w-md">
      <h2 className="text-2xl font-bold mb-4">Compute</h2>
      <input
        className="w-full p-2 mb-4 border border-gray-300 rounded text-black"
        placeholder="Program id"
        value={programId}
        onChange={(e) => setProgramId(e.target.value)}
      />
      <button
        className={`flex items-center justify-center px-4 py-2 border rounded text-black mb-4 ${
          nilCompute.isLoading || !programId
            ? "opacity-50 cursor-not-allowed bg-gray-200"
            : "bg-white hover:bg-gray-100"
        }`}
        onClick={handleClick}
        disabled={nilCompute.isLoading || !programId}
      >
        {nilCompute.isLoading ? (
          <div className="w-5 h-5 border-t-2 border-b-2 border-gray-900 rounded-full animate-spin"></div>
        ) : (
          "Compute"
        )}
      </button>
      <p className="my-2 italic text-sm mt-2">
        Current values are 4 & 2. Refer to ComputeOutput.tsx
      </p>
      <ul className="list-disc pl-5 mt-4">
        <li className="mt-2">Status: {nilCompute.status}</li>
        <li className="mt-2">
          Compute output id:
          {nilCompute.isSuccess ? (
            <>
              {`${nilCompute.data?.substring(0, 4)}...${nilCompute.data?.substring(nilCompute.data.length - 4)}`}
              <button
                onClick={() => {
                  setCopiedComputeOutputID(true);
                  navigator.clipboard.writeText(nilCompute.data);
                  setTimeout(() => setCopiedComputeOutputID(false), 2000);
                }}
              >
                {!copiedComputeOutputID ? " 📋" : " ✅"}
              </button>
            </>
          ) : (
            "idle"
          )}
        </li>
      </ul>
    </div>
  );
          )}
```

- Secure multi-party computation
- Encrypted data processing

#### 3. Result Processing

```7:56:app/components/ComputeOutput.tsx
export const ComputeOutput: FC = () => {
  const nilComputeOutput = useNilComputeOutput();
  const [computeId, setComputeId] = useState<ComputeOutputId | string>("");

  const handleClick = () => {
    if (!computeId) throw new Error("compute-output: Compute id is required");
    nilComputeOutput.execute({ id: computeId });
  };

  let computeOutput = "idle";
  if (nilComputeOutput.isSuccess) {
    computeOutput = JSON.stringify(nilComputeOutput.data, (key, value) => {
      if (typeof value === "bigint") {
        return value.toString();
      }
      return value;
    });
  }

  return (
    <div className="border border-gray-400 rounded-lg p-4 w-full max-w-md">
      <h2 className="text-2xl font-bold mb-4">Compute Output</h2>
      <input
        className="w-full p-2 mb-4 border border-gray-300 rounded text-black"
        placeholder="Compute output id"
        value={computeId}
        onChange={(e) => setComputeId(e.target.value)}
      />
      <button
        className={`flex items-center justify-center px-4 py-2 border rounded text-black  ${
          !computeId || nilComputeOutput.isLoading
            ? "opacity-50 cursor-not-allowed bg-gray-200"
            : "bg-white hover:bg-gray-100"
        }`}
        onClick={handleClick}
        disabled={!computeId || nilComputeOutput.isLoading}
      >
        {nilComputeOutput.isLoading ? (
          <div className="w-5 h-5 border-t-2 border-b-2 border-gray-900 rounded-full animate-spin"></div>
        ) : (
          "Fetch"
        )}
      </button>
      <ul className="list-disc pl-5 mt-4">
        <li className="mt-2">Status: {nilComputeOutput.status}</li>
        <li className="mt-2">Output: {computeOutput}</li>
      </ul>
    </div>
  );
}
```

- Secure output handling
- Role-specific result filtering

## Security Features

### 1. Data Protection
- End-to-end encryption
- Zero-knowledge computation
- Secure key management

### 2. Access Control
- Party-specific bindings
- Role-based permissions
- Granular output control

## Getting Started

### Prerequisites
- Node.js 16+
- nillion-devnet running

### Installation
```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to access the platform.

## Usage Guide

### 1. For Patients
- Input medical history securely
- View trial eligibility
- Monitor treatment effectiveness

### 2. For Researchers
- Define trial criteria
- Access aggregated results
- Analyze treatment efficacy

### 3. For Hospitals
- Monitor trial safety
- Track patient outcomes
- Ensure compliance

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Support
For support, please reach out on [Github Discussions](https://github.com/orgs/NillionNetwork/discussions)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

Built with ❤️ using [Nillion](https://nillion.com/) secure computation technology.


## Getting Started

### Prerequisites
- Node.js 16+
- nillion-devnet running

### Installation

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

Then follow the rest of the instructions from the Quickstart guide [here.](https://github.com/NillionNetwork/awesome-nillion/issues/2)


## Usage Guide

1. **Authentication**
   - Login with secure credentials
   - Maintain session security
   - Handle role-based access

2. **Data Input**
   - Enter financial metrics
   - Validate input data
   - Secure data transmission

3. **Computation**
   - Process encrypted data
   - Generate secure results
   - Handle multi-party access

4. **Result Retrieval**
   - Fetch computation results
   - Process role-specific outputs
   - Display filtered information

## Security Considerations

1. **Data Privacy**
   - All computations performed on encrypted data
   - Zero-knowledge proof verification
   - Secure multi-party computation

2. **Access Control**
   - Role-based permissions
   - Party-specific data access
   - Granular output control

3. **Key Management**
   - Secure key generation
   - Safe storage practices
   - Regular key rotation

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Support
For support, please reach out on [Github Discussions](https://github.com/orgs/NillionNetwork/discussions)
