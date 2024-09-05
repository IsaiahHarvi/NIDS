import React, { useEffect } from "react";
import { getSavedAttacks } from "../middleware/api/functions/getSavedAttacks";
import { useClientStore } from "../stores/client-store";
// import {
//   Card,
//   CardHeader,
//   CardTitle,
//   CardContent,
//   CardDescription,
// } from "./Card";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "./ui/card";

const AttackControl: React.FC = () => {
  const { savedAttacks, setSavedAttacks } = useClientStore();

  useEffect(() => {
    getSavedAttacks().then((m) => {
      if (m !== null) {
        setSavedAttacks(m);
      }
    });
  }, [setSavedAttacks]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Attack Control</h1>
      <div>
        <h2 className="text-xl font-semibold mb-2">Saved Attacks</h2>
        <ul className="space-y-4">
          {savedAttacks.map((attack) => (
            <li key={attack.attackId}>
              <Card>
                <CardHeader>
                  <CardTitle>{attack.name}</CardTitle>
                  <CardDescription>{attack.severity} Severity</CardDescription>
                </CardHeader>
                <CardContent>
                  <p>{attack.description}</p>
                  <p>
                    <strong>Source IP:</strong> {attack.sourceIp}
                  </p>
                  <p>
                    <strong>Destination IP:</strong> {attack.destinationIp}
                  </p>
                  <p>
                    <strong>Protocol:</strong> {attack.protocol}
                  </p>
                  <p>
                    <strong>Detected:</strong> {attack.detected ? "Yes" : "No"}
                  </p>
                  <div className="mt-2">
                    <h4 className="font-semibold">Mitigation Actions:</h4>
                    <ul className="list-disc list-inside">
                      {attack.mitigationActions.map((action, index) => (
                        <li key={index}>{action}</li>
                      ))}
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AttackControl;
